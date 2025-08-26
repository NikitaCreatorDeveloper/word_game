<<<<<<< HEAD
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
=======
# Word Game Kivy 🎮

Мини-игра на Kivy: угадай слово с ограничением по попыткам.  
Проект доведён до уровня: полноценные настройки, анимации, звуки, словари по категориям и dev-инфра.

---

## ✨ Возможности
- 🎨 Темы: светлая и тёмная (применяются мгновенно)
- 🔤 Масштаб шрифта (1.0× / 1.25× / 1.5×)
- ⏱ Таймер раунда:
  - вкл/выкл
  - выбор длины (30/60/90/120 секунд)
- 🎮 Уровни сложности:
  - Easy (10 попыток, простые слова)
  - Normal (8 попыток, средние слова)
  - Hard (6 попыток, редкие слова)
- 📚 Категории слов:
  - Animals, Food, Countries (по 50 слов в каждой категории и сложности)
- 🎹 Горячие клавиши:
  - Esc — вернуться в меню
  - Ctrl+N — новое слово
- 🔊 Щелчки на каждом действии (можно отключить в настройках)
- 🌀 Анимация: мерцание слова при победе/поражении
- 📊 Сохранение профиля, очков, побед/поражений
- 🛠 Dev-инфра: `ruff`, `black`, `mypy`, `pytest`, GitHub Actions CI

---

## 📸 Скриншоты и демо
![Меню](docs/screenshots/menu.png)  
![Категории](docs/screenshots/category.png)  
![Игра](docs/screenshots/game.png)  
![Победа](docs/screenshots/win.png)  
![Поражение](docs/screenshots/lose.png)  

### 🎥 Демо
![Демо](docs/screenshots/demo.gif)

---

## 🚀 Установка и запуск
```bash
git clone https://github.com/<username>/word_game_kivy.git
cd word_game_kivy

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
>>>>>>> 6fdce8c (style: apply ruff/black auto-fixes)
source .venv/bin/activate

pip install -r requirements.txt

python -m word_game_kivy.main
```

<<<<<<< HEAD
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

=======
---

## 🧪 Тесты и разработка
>>>>>>> 6fdce8c (style: apply ruff/black auto-fixes)
```bash
pip install -r requirements-dev.txt
pytest -q
```

<<<<<<< HEAD
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
=======
- `ruff`, `black`, `mypy` запускаются автоматически через pre-commit
- GitHub Actions CI прогоняет линтеры и тесты при каждом push

---

## 🗺 Roadmap
- [x] Система профилей
- [x] Таблица лидеров
- [x] Настройки: тема, таймер (вкл/выкл и длина), масштаб
- [x] Уровни сложности с отдельными словарями
- [x] Категории слов по 50 слов в каждой
- [x] Звуки и анимации
- [ ] Экспорт лидерборда
- [ ] Бандл под Android (Buildozer)

---

## 📜 Лицензия
MIT © 2025 Nikita Creator
>>>>>>> 6fdce8c (style: apply ruff/black auto-fixes)
