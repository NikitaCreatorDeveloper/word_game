import json
import os

from game.player import Player


def load_players():
    if os.path.exists("data/players.json"):
        try:
            with open("data/players.json", "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return {
                    name: Player.from_dict(name, data)
                    for name, data in raw_data.items()
                }
        except json.JSONDecodeError:
            print("⚠️ Файл повреждён. Начинаем заново.")
            return {}
    return {}


def save_players(players):
    os.makedirs("data", exist_ok=True)
    with open("data/players.json", "w", encoding="utf-8") as f:
        json.dump(
            {name: player.to_dict() for name, player in players.items()}, f, indent=4
        )
