from __future__ import annotations
from typing import Literal
from .storage import DATA_DIR, load_json, save_json

PROFILE_PATH = DATA_DIR / "profile.json"


def _load_profile() -> dict:
    return load_json(PROFILE_PATH, {})


def _save_profile(data: dict) -> None:
    save_json(PROFILE_PATH, data)


# --- Theme ---
def get_theme() -> Literal["dark", "light"]:
    return _load_profile().get("theme", "dark")


def set_theme(theme: str) -> None:
    data = _load_profile()
    data["theme"] = "light" if theme == "light" else "dark"
    _save_profile(data)


# --- Font scale ---
def get_font_scale() -> float:
    try:
        return float(_load_profile().get("font_scale", 1.0))
    except Exception:
        return 1.0


def set_font_scale(scale: float) -> None:
    data = _load_profile()
    data["font_scale"] = float(scale)
    _save_profile(data)


# --- Timer on/off ---
def get_timer_enabled() -> bool:
    return bool(_load_profile().get("timer_enabled", False))


def set_timer_enabled(enabled: bool) -> None:
    data = _load_profile()
    data["timer_enabled"] = bool(enabled)
    _save_profile(data)


# --- Timer length (seconds) ---
def get_timer_seconds() -> int:
    try:
        return int(_load_profile().get("timer_seconds", 60))
    except Exception:
        return 60


def set_timer_seconds(seconds: int) -> None:
    data = _load_profile()
    data["timer_seconds"] = max(5, int(seconds))
    _save_profile(data)


# --- Letter bonus ---
def get_letter_bonus() -> int:
    try:
        return int(_load_profile().get("letter_bonus", 10))
    except Exception:
        return 10


def set_letter_bonus(bonus: int) -> None:
    data = _load_profile()
    data["letter_bonus"] = max(0, int(bonus))
    _save_profile(data)


# --- Difficulty ---
def get_difficulty() -> str:
    # 'easy' | 'normal' | 'hard'
    return _load_profile().get("difficulty", "normal")


def set_difficulty(diff: str) -> None:
    diff = diff.lower()
    if diff not in ("easy", "normal", "hard"):
        diff = "normal"
    data = _load_profile()
    data["difficulty"] = diff
    _save_profile(data)


# --- Sound on/off ---
def get_sfx_enabled() -> bool:
    return bool(_load_profile().get("sfx_enabled", True))


def set_sfx_enabled(enabled: bool) -> None:
    data = _load_profile()
    data["sfx_enabled"] = bool(enabled)
    _save_profile(data)
