# Word Game Kivy

Небольшая игра на **Kivy (Python)** с многоэкранной навигацией, локальным сохранением, таблицей рекордов, звуками и кастомными виджетами.

---

## 🧭 Обзор

Игрок вводит имя, выбирает категорию и отгадывает слово. Прогресс и статистика сохраняются локально (JSON). Есть таблица лидеров с суммарными победами/поражениями и очками. Интерфейс использует переиспользуемые виджеты (`FancyButton`) и базовые элементы экранов.

---

## ✨ Фичи

- Поток экранов: Имя → Меню → Категории → Игра → Лидерборд.
- Локальное хранение (JSON) для игроков и статистики.
- Таблица лидеров (очки / победы / поражения).
- Звуковые эффекты (клик / победа / поражение).
- Кастомные анимированные кнопки (`FancyButton`) и общие вспомогатели для UI.
- CI GitHub Actions; инструменты разработки (Ruff, Black, isort, pytest).

---

## 🗂 Структура проекта

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

> **Примечание:** В проекте есть ссылки на `assets/...`. Добавьте ассеты или обновите пути.

---

## ▶️ Запуск (Desktop)

**Предварительно:** Python 3.11+, pip, рекомендован virtualenv.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

python -m word_game_kivy.main
```

Если Kivy не стартует, смотрите инструкции: <https://kivy.org/doc/stable/gettingstarted/installation.html>

---

## 📱 Android (Buildozer)

Требуется Linux или WSL (Windows).

```bash
pip install buildozer
buildozer init     # уже есть в репо
buildozer android debug
# APK появится в папке bin/
```

---

## 🧪 Тесты

```bash
pip install -r requirements-dev.txt
pytest -q
```

---

## ⚙️ Инструменты

- **Ruff / Black / isort** — линт и форматирование
- **pytest** — тесты
- **GitHub Actions** — CI

---

## 🗺 План доработок

- [ ] Добавить папку `assets` (шрифты, звуки) или сделать пути настраиваемыми.
- [ ] Завершить части кода, где оставлены заглушки (`...`).
- [ ] Добавить типизацию и docstrings.
- [ ] Расширить тесты: игровой поток, сортировка лидерборда, поведение виджетов.
- [ ] Локализация (EN/RU) для текста интерфейса.
- [ ] Экран настроек (звук, сложность).
- [ ] Пакетирование или страница itch.io + скриншоты/GIF.

---

## 📝 Лицензия

MIT — см. `LICENSE`.
