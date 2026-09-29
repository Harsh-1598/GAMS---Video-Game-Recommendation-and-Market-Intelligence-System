"""Common title aliases used when a user enters a played game."""

from __future__ import annotations

import re


TITLE_ALIASES = {
    "gta": "Grand Theft Auto",
    "gta 3": "Grand Theft Auto III",
    "gta iii": "Grand Theft Auto III",
    "gta 4": "Grand Theft Auto IV",
    "gta iv": "Grand Theft Auto IV",
    "gta 5": "Grand Theft Auto V",
    "gta v": "Grand Theft Auto V",
    "gta san andreas": "Grand Theft Auto: San Andreas",
    "gta sa": "Grand Theft Auto: San Andreas",
    "gta vice city": "Grand Theft Auto: Vice City",
    "cod": "Call of Duty",
    "call of duty mw": "Call of Duty 4: Modern Warfare",
    "cod 4": "Call of Duty 4: Modern Warfare",
    "cod mw": "Call of Duty 4: Modern Warfare",
    "cod mw2": "Call of Duty: Modern Warfare 2",
    "cod mw3": "Call of Duty: Modern Warfare 3",
    "cod black ops": "Call of Duty: Black Ops",
    "cod bo": "Call of Duty: Black Ops",
    "black ops": "Call of Duty: Black Ops",
    "cod world at war": "Call of Duty: World at War",
    "ac": "Assassin's Creed",
    "assassins creed 2": "Assassin's Creed II",
    "ac2": "Assassin's Creed II",
    "assassins creed 3": "Assassin's Creed III",
    "ac3": "Assassin's Creed III",
    "assassins creed iv": "Assassin's Creed IV: Black Flag",
    "ac4": "Assassin's Creed IV: Black Flag",
    "assassins creed black flag": "Assassin's Creed IV: Black Flag",
    "rdr": "Red Dead Redemption",
    "red dead 1": "Red Dead Redemption",
    "red dead redemption 2": "Red Dead Redemption 2",
    "mario": "Super Mario Bros.",
    "super mario": "Super Mario Bros.",
    "mario kart": "Mario Kart Wii",
    "mario kart wii": "Mario Kart Wii",
    "mario 64": "Super Mario 64",
    "super mario 64": "Super Mario 64",
    "mario galaxy": "Super Mario Galaxy",
    "mario galaxy 2": "Super Mario Galaxy 2",
    "zelda": "The Legend of Zelda",
    "legend of zelda": "The Legend of Zelda",
    "ocarina of time": "The Legend of Zelda: Ocarina of Time",
    "zelda oot": "The Legend of Zelda: Ocarina of Time",
    "breath of the wild": "The Legend of Zelda: Breath of the Wild",
    "botw": "The Legend of Zelda: Breath of the Wild",
    "pokemon": "Pokemon Red/Pokemon Blue",
    "pokemon red": "Pokemon Red/Pokemon Blue",
    "pokemon blue": "Pokemon Red/Pokemon Blue",
    "pokemon gold": "Pokemon Gold/Pokemon Silver",
    "pokemon silver": "Pokemon Gold/Pokemon Silver",
    "halo": "Halo: Combat Evolved",
    "halo ce": "Halo: Combat Evolved",
    "halo 2": "Halo 2",
    "halo 3": "Halo 3",
    "halo reach": "Halo: Reach",
    "battlefield": "Battlefield 3",
    "bf3": "Battlefield 3",
    "bf4": "Battlefield 4",
    "need for speed": "Need for Speed: Most Wanted",
    "nfs most wanted": "Need for Speed: Most Wanted",
    "nfs mw": "Need for Speed: Most Wanted",
    "fifa": "FIFA 14",
    "fifa 14": "FIFA 14",
    "fifa 15": "FIFA 15",
    "fifa 16": "FIFA 16",
    "nba 2k": "NBA 2K14",
    "nba 2k14": "NBA 2K14",
    "madden": "Madden NFL 2004",
    "mortal kombat": "Mortal Kombat",
    "street fighter": "Street Fighter IV",
    "tekken": "Tekken 3",
    "final fantasy": "Final Fantasy VII",
    "final fantasy 7": "Final Fantasy VII",
    "ff7": "Final Fantasy VII",
    "skyrim": "The Elder Scrolls V: Skyrim",
    "elder scrolls skyrim": "The Elder Scrolls V: Skyrim",
    "fallout 3": "Fallout 3",
    "fallout new vegas": "Fallout: New Vegas",
    "minecraft": "Minecraft",
    "portal": "Portal 2",
    "portal 2": "Portal 2",
    "counter strike": "Counter-Strike",
    "cs": "Counter-Strike",
    "team fortress 2": "Team Fortress 2",
    "tf2": "Team Fortress 2",
    "left 4 dead": "Left 4 Dead",
    "left 4 dead 2": "Left 4 Dead 2",
    "resident evil 4": "Resident Evil 4",
    "re4": "Resident Evil 4",
    "metal gear solid": "Metal Gear Solid",
    "mgsv": "Metal Gear Solid V: The Phantom Pain",
    "god of war": "God of War",
    "uncharted": "Uncharted 2: Among Thieves",
    "crash bandicoot": "Crash Bandicoot 2: Cortex Strikes Back",
    "sonic": "Sonic the Hedgehog",
    "sims": "The Sims 3",
    "the sims": "The Sims 3",
}

PLATFORM_ALIASES = {
    "pc": "PC",
    "windows": "PC",
    "computer": "PC",
    "playstation": "PS",
    "sony playstation": "PS",
    "ps1": "PS",
    "ps one": "PS",
    "psx": "PS",
    "ps2": "PS",
    "playstation 2": "PS",
    "ps3": "PS",
    "playstation 3": "PS",
    "ps4": "PS",
    "playstation 4": "PS",
    "ps5": "PS",
    "playstation 5": "PS",
    "xbox": "XBOX",
    "xbox 360": "XBOX",
    "xbox one": "XBOX",
    "nintendo": "Nintendo",
    "switch": "Nintendo",
}


def normalize_title(value: object) -> str:
    """Normalize a title for exact catalog matching."""

    value = str(value).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_platform(value: object) -> str:
    """Map common user-facing platform names to catalog platform families."""

    normalized = normalize_title(value)
    return PLATFORM_ALIASES.get(normalized, str(value).strip())


def resolve_title(query: str, catalog_titles: list[str]) -> str | None:
    """Resolve an alias or normalized title to a catalog title."""

    normalized_query = normalize_title(query)
    alias = TITLE_ALIASES.get(normalized_query, query)
    normalized_alias = normalize_title(alias)
    normalized_catalog = {
        normalize_title(title): title for title in catalog_titles
    }

    if normalized_alias in normalized_catalog:
        return normalized_catalog[normalized_alias]

    partial_matches = [
        title for normalized, title in normalized_catalog.items()
        if normalized_alias in normalized or normalized in normalized_alias
    ]
    return partial_matches[0] if len(partial_matches) == 1 else None
