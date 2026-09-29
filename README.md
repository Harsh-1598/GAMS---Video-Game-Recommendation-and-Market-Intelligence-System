# GAMS

This project trains metadata-based machine-learning models that predict global
game sales and ranks recommendations for a game the user has played. It also
supports filter-only discovery when no seed game is supplied.

The web app supports two platform modes:

- `Any platform`: recommendations can come from the full catalog.
- `Use one platform`: recommendations are restricted to the played or selected platform.
- A played game produces a metadata similarity score and a recommendation score.
- Genre, publisher, and release-decade filters can be used without a played game.

## Run the website

From the project directory:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

The model search runs once when the backend starts. It compares tuned Random
Forest and Extra Trees regressors with cross-validation, then keeps the better
candidate. The API exposes:

- `GET /api/health`
- `GET /api/options`
- `POST /api/recommend`

The notebook remains available for exploration and model analysis. The web
frontend is served by FastAPI, so no separate frontend server is needed.
