"""Training, tuning, and inference for the game recommendation engine."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .aliases import normalize_platform, resolve_title


class GameRecommendationEngine:
    def __init__(self, data_path: str | Path):
        self.data = self._load_and_clean(data_path)
        self.model_features = [
            "Platform", "Genre", "Publisher", "Year_For_Feature", "Release_Decade"
        ]
        self.categorical_features = [
            "Platform", "Genre", "Publisher", "Release_Decade"
        ]
        self.numeric_features = ["Year_For_Feature"]
        self.model = None
        self.model_name = ""
        self.metrics = {}
        self._train_and_tune()

    @staticmethod
    def _load_and_clean(data_path: str | Path) -> pd.DataFrame:
        data = pd.read_csv(data_path)
        data.columns = data.columns.str.strip()
        required = {
            "Rank", "Name", "Platform", "Year", "Genre", "Publisher",
            "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales",
        }
        missing = sorted(required - set(data.columns))
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        categorical = ["Name", "Platform", "Genre", "Publisher"]
        numeric = [
            "Rank", "Year", "NA_Sales", "EU_Sales", "JP_Sales",
            "Other_Sales", "Global_Sales",
        ]
        missing_tokens = {"", "n/a", "na", "null", "none", "unknown"}

        for column in categorical:
            data[column] = data[column].map(
                lambda value: value.strip() if isinstance(value, str) else value
            )
            data[column] = data[column].map(
                lambda value: pd.NA
                if isinstance(value, str) and value.lower() in missing_tokens
                else value
            )
        for column in numeric:
            data[column] = pd.to_numeric(data[column], errors="coerce")

        sales = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
        data = data.drop_duplicates()
        data = data.loc[~data[sales].lt(0).any(axis=1)]
        data = data.dropna(subset=["Name", "Global_Sales"]).copy()
        data["Year"] = data["Year"].round().astype("Int64")
        for column in ["Platform", "Genre", "Publisher"]:
            data[column] = data[column].fillna("Unknown").astype("string")
        data["Name"] = data["Name"].astype("string")

        platform_groups = {
            value: "PS" for value in ["PS", "PS2", "PS3", "PS4", "PS5", "PSV", "PSP"]
        }
        platform_groups.update({value: "XBOX" for value in ["X360", "XOne", "XBOX", "XS", "XB"]})
        platform_groups.update({value: "Nintendo" for value in ["Wii", "WiiU", "DS", "3DS", "Switch", "GBA", "GC", "N64", "SNES", "NES", "GB", "GBC"]})
        platform_groups.update({value: "Sega" for value in ["GEN", "SCD", "SAT", "DC", "GG"]})
        platform_groups.update({value: "Atari" for value in ["2600", "5200", "7800", "Lynx", "Jaguar"]})
        platform_groups.update({value: "Others" for value in ["NeoGeo", "TG16", "3DO", "WS", "VB", "PCFX", "NG"]})
        data["Platform"] = data["Platform"].replace(platform_groups)

        data["Year_For_Feature"] = data["Year"].fillna(data["Year"].median()).astype(int)
        data["Release_Decade"] = (data["Year_For_Feature"] // 10 * 10).astype(str)
        data["Log_Global_Sales"] = np.log1p(data["Global_Sales"])
        return data.reset_index(drop=True)

    def _pipeline(self, estimator) -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore"),
                    self.categorical_features,
                ),
                (
                    "numeric",
                    Pipeline([
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]),
                    self.numeric_features,
                ),
            ]
        )
        return Pipeline([("preprocessor", preprocessor), ("model", estimator)])

    def _train_and_tune(self) -> None:
        train_index, test_index = train_test_split(
            self.data.index, test_size=0.2, random_state=42
        )
        X_train = self.data.loc[train_index, self.model_features]
        X_test = self.data.loc[test_index, self.model_features]
        y_train = self.data.loc[train_index, "Log_Global_Sales"]
        y_test = self.data.loc[test_index, "Global_Sales"]

        # Vercel should start from the parameters selected during local tuning.
        # Running cross-validation during every serverless cold start is too slow.
        if os.getenv("VERCEL") == "1":
            self.model = self._pipeline(
                RandomForestRegressor(
                    n_estimators=150,
                    max_depth=35,
                    min_samples_leaf=2,
                    random_state=42,
                    n_jobs=-1,
                )
            )
            self.model.fit(X_train, y_train)
            predictions = np.maximum(np.expm1(self.model.predict(X_test)), 0)
            self.model_name = "RandomForestRegressor"
            self.metrics = {
                "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
                "rmse": round(float(np.sqrt(mean_squared_error(y_test, predictions))), 4),
                "r2": round(float(r2_score(y_test, predictions)), 4),
                "cv_rmse": None,
                "best_params": {
                    "model__n_estimators": 150,
                    "model__max_depth": 35,
                    "model__min_samples_leaf": 2,
                },
            }
            return

        candidates = [
            (
                "RandomForestRegressor",
                self._pipeline(RandomForestRegressor(random_state=42, n_jobs=-1)),
                {
                    "model__n_estimators": [150, 250],
                    "model__max_depth": [None, 20, 35],
                    "model__min_samples_leaf": [1, 2],
                },
            ),
            (
                "ExtraTreesRegressor",
                self._pipeline(ExtraTreesRegressor(random_state=42, n_jobs=-1)),
                {
                    "model__n_estimators": [150, 250],
                    "model__max_depth": [None, 20, 35],
                    "model__min_samples_leaf": [1, 2],
                },
            ),
        ]

        best_search = None
        best_name = ""
        for name, pipeline, parameters in candidates:
            search = RandomizedSearchCV(
                pipeline,
                parameters,
                n_iter=6,
                scoring="neg_root_mean_squared_error",
                cv=3,
                random_state=42,
                n_jobs=-1,
                refit=True,
            )
            search.fit(X_train, y_train)
            if best_search is None or search.best_score_ > best_search.best_score_:
                best_search = search
                best_name = name

        self.model = best_search.best_estimator_
        self.model_name = best_name
        predictions = np.maximum(np.expm1(self.model.predict(X_test)), 0)
        self.metrics = {
            "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
            "rmse": round(float(np.sqrt(mean_squared_error(y_test, predictions))), 4),
            "r2": round(float(r2_score(y_test, predictions)), 4),
            "cv_rmse": round(float(-best_search.best_score_), 4),
            "best_params": best_search.best_params_,
        }

    def options(self) -> dict[str, list[str]]:
        return {
            "platforms": sorted(self.data["Platform"].dropna().unique().tolist()),
            "genres": sorted(self.data["Genre"].dropna().unique().tolist()),
            "publishers": sorted(self.data["Publisher"].dropna().unique().tolist()),
            "decades": sorted(self.data["Release_Decade"].unique().tolist()),
        }

    def _find_played_game(self, title: str, platform: str | None) -> pd.Series:
        catalog_title = resolve_title(title, self.data["Name"].tolist())
        if catalog_title is None:
            raise ValueError("Played game was not found in the catalog. Try a fuller title.")
        matches = self.data[self.data["Name"] == catalog_title]
        if platform:
            selected_platform = normalize_platform(platform).lower()
            platform_matches = matches[
                matches["Platform"].str.lower() == selected_platform
            ]
            if not platform_matches.empty:
                matches = platform_matches
            # A title can exist in the catalog without a release on the chosen
            # platform. Keep the title as the seed and apply platform filtering
            # to the recommendations instead of rejecting the whole request.
        return matches.iloc[0]

    def recommend(
        self,
        title: str | None = None,
        played_platform: str | None = None,
        platform_mode: str = "any",
        selected_platform: str | None = None,
        genre: str | None = None,
        publisher: str | None = None,
        release_decade: str | None = None,
        limit: int = 10,
    ) -> dict:
        if platform_mode not in {"any", "same"}:
            raise ValueError("platform_mode must be 'any' or 'same'.")
        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50.")
        if not title and not any([genre, publisher, release_decade]):
            raise ValueError("Provide a played game or at least one filter.")

        seed = self._find_played_game(title, played_platform) if title else None
        candidates = self.data.copy()
        if seed is not None:
            candidates = candidates[candidates["Name"] != seed["Name"]]
        if platform_mode == "same":
            target_platform = normalize_platform(selected_platform or played_platform) if (selected_platform or played_platform) else None
            if not target_platform:
                raise ValueError("A platform is required in same-platform mode.")
            candidates = candidates[
                candidates["Platform"].str.lower() == target_platform.lower()
            ]
        if genre:
            candidates = candidates[candidates["Genre"].str.lower() == genre.lower()]
        if publisher:
            candidates = candidates[candidates["Publisher"].str.lower() == publisher.lower()]
        if release_decade:
            candidates = candidates[candidates["Release_Decade"] == str(release_decade)]
        if candidates.empty:
            return {"played_game": seed["Name"] if seed is not None else None, "results": []}

        candidates = candidates.copy()
        candidates["Predicted_Global_Sales"] = np.maximum(
            np.expm1(self.model.predict(candidates[self.model_features])), 0
        )
        target_genre = seed["Genre"] if seed is not None else genre
        target_publisher = seed["Publisher"] if seed is not None else publisher
        target_decade = seed["Release_Decade"] if seed is not None else release_decade
        matches = []
        weights = []
        if target_genre:
            matches.append((candidates["Genre"] == target_genre).astype(float))
            weights.append(0.50)
        if target_publisher:
            matches.append((candidates["Publisher"] == target_publisher).astype(float))
            weights.append(0.30)
        if target_decade:
            matches.append((candidates["Release_Decade"] == str(target_decade)).astype(float))
            weights.append(0.20)
        candidates["Similarity_Score"] = sum(
            weight * match for weight, match in zip(weights, matches)
        ) / sum(weights)
        sales_rank = candidates["Predicted_Global_Sales"].rank(pct=True)
        candidates["Recommendation_Score"] = (
            0.70 * candidates["Similarity_Score"] + 0.30 * sales_rank
        )
        results = candidates.sort_values(
            ["Recommendation_Score", "Predicted_Global_Sales"],
            ascending=False,
        ).drop_duplicates("Name").head(limit)
        columns = [
            "Name", "Platform", "Genre", "Publisher", "Year",
            "Predicted_Global_Sales", "Similarity_Score", "Recommendation_Score",
        ]
        output = results[columns].astype(object).where(pd.notna(results[columns]), None)
        records = output.to_dict(orient="records")
        for record in records:
            record["Similarity_Score"] = round(float(record["Similarity_Score"]) * 100, 1)
            record["Recommendation_Score"] = round(float(record["Recommendation_Score"]) * 100, 1)
            record["Predicted_Global_Sales"] = round(float(record["Predicted_Global_Sales"]), 2)
        return {"played_game": seed["Name"] if seed is not None else None, "results": records}
