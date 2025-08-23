# Word Game Kivy

A compact word‑guessing game built with **Kivy (Python)** featuring a multi‑screen flow, local persistence, a leaderboard, sound effects, and custom animated widgets.

---

## 🧭 Overview

The app lets a player enter their name, pick a category, and guess a word. Progress and stats are saved locally (JSON). There’s a leaderboard aggregating wins/losses and score. The UI is composed of reusable widgets (e.g., `FancyButton`) and base screen helpers.

---

## ✨ Features

- ScreenManager flow: Name → Menu → Category → Game → Leaderboard.
- Local JSON storage for players and stats.
- Leaderboard with sortable scores (wins/losses/points).
- Sound effects (click / win / lose).
- Custom animated buttons (`FancyButton`) and shared UI helpers.
- CI via GitHub Actions; dev tooling (Ruff, Black, isort, pytest).

---

## 🗂 Project Structure

```txt
word_game_kivy/
  word_game_kivy/
    game/
      player.py
    screens/
      base_screen.py
      name_screen.py
      menu_screen.py
      category_screen.py
      game_screen.py
      leaderboard_screen.py
    utils/
      storage.py
    widgets/
      fancy_button.py
    main.py
  requirements.txt
  requirements-dev.txt
  buildozer.spec
  tests/
  .github/workflows/ci.yml
```

> **Note:** The repository currently references assets (fonts, sounds) under `assets/...`. Make sure to add them or adjust code paths.

---

## ▶️ Run (Desktop)

**Prereqs:** Python 3.11+, pip, virtualenv recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

python -m word_game_kivy.main
```

If Kivy fails to start, check: <https://kivy.org/doc/stable/gettingstarted/installation.html>

---

## 📱 Android (Buildozer)

Requires Linux host or WSL (Windows).

```bash
pip install buildozer
buildozer init     # already present in repo
buildozer android debug
# APK will appear under bin/
```

---

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

---

## ⚙️ Tooling

- **Ruff / Black / isort** for lint & format
- **pytest** for tests
- **GitHub Actions** for CI

---

## 🗺 Roadmap

- [ ] Add assets folder (fonts, SFX) or make paths configurable.
- [ ] Finish/verify missing parts in several screens where placeholders were used (`...`).
- [ ] Add type hints & docstrings across modules.
- [ ] Expand tests: game flow, leaderboard sorting, widget behavior.
- [ ] i18n (EN/RU) for UI text.
- [ ] In‑app settings (sound, difficulty).
- [ ] Packaging or itch.io page + screenshots/GIF.

---

## 📝 License

MIT — see `LICENSE`.
