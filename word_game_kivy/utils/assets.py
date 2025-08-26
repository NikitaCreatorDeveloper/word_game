from pathlib import Path


def get_asset_path(rel: str) -> str:
    """Return absolute path to an asset, whether run from repo root or package folder."""
    base = Path(__file__).resolve()
    pkg = base
    for _ in range(7):
        if (pkg / "assets").exists() or (pkg / "word_game_kivy" / "assets").exists():
            break
        pkg = pkg.parent
    cand1 = (
        (pkg / "assets" / Path(rel).name) if rel.startswith("assets/") else (pkg / rel)
    )
    cand2 = pkg / "word_game_kivy" / rel
    # Prefer exact rel path first
    exact1 = pkg / rel
    if exact1.exists():
        return str(exact1)
    if cand1.exists():
        return str(cand1)
    if cand2.exists():
        return str(cand2)
    return str(exact1)  # may not exist; callers should handle
