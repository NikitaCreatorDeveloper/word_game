from word_game_kivy.utils.storage import load_json
from pathlib import Path


def test_load_json_corrupted(tmp_path: Path):
    p = tmp_path / "broken.json"
    p.write_text("{not-json", encoding="utf-8")
    data = load_json(p, default={"ok": True})
    assert data == {"ok": True}
