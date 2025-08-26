from __future__ import annotations

import json
from typing import Any, Dict, Union
from pathlib import Path

from ..game.player import Player

# Храним data внутри пакета: .../word_game_kivy/data
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PLAYERS_PATH = DATA_DIR / "players.json"


def load_json(
    path: str | Path, default: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return default or {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default or {}


def save_json(path: str | Path, data: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_players() -> Dict[str, Player]:
    """Загрузить игроков из JSON -> словарь name -> Player."""
    raw: Dict[str, Any] = load_json(PLAYERS_PATH, {})
    out: Dict[str, Player] = {}
    for name, rec in raw.items():
        if isinstance(rec, dict):
            # Нормальный случай: словарь -> Player
            try:
                out[name] = Player.from_dict(rec)
            except Exception:
                # пропускаем битые записи
                continue
        elif isinstance(rec, Player):
            # На всякий: если кто-то уже положил Player
            out[name] = rec
        else:
            # мусор — пропускаем
            continue
    return out


def save_players(players: Dict[str, Union[Player, Dict[str, Any]]]) -> None:
    """Сохранить словарь name -> Player как JSON (to_dict). Допускаем dict для совместимости."""
    serializable: Dict[str, Dict[str, Any]] = {}
    for name, obj in players.items():
        if isinstance(obj, Player):
            serializable[name] = obj.to_dict()
        elif isinstance(obj, dict):
            serializable[name] = obj
        else:
            # игнор мусора
            continue
    save_json(PLAYERS_PATH, serializable)
