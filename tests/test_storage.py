import shutil
from pathlib import Path

from word_game_kivy.game.player import Player
from word_game_kivy.utils.storage import load_players, save_players


def test_save_and_load_players(tmp_path):
    # Работаем с реальным файлом в репо: word_game_kivy/data/players.json
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "word_game_kivy" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    target = data_dir / "players.json"
    backup = None

    if target.exists():
        backup = tmp_path / "players.backup.json"
        shutil.copyfile(target, backup)

    try:
        players = {"Alice": Player("Alice"), "Bob": Player("Bob")}
        players["Alice"].score = 10
        players["Bob"].score = 5

        save_players(players)
        loaded = load_players()

        assert set(loaded.keys()) == {"Alice", "Bob"}
        assert loaded["Alice"].score == 10
        assert loaded["Bob"].score == 5
    finally:
        if target.exists():
            target.unlink()
        if backup and backup.exists():
            shutil.copyfile(backup, target)
