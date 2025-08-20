# Word Game Kivy

Небольшая игра на **Kivy (Python)** с меню, выбором категорий, таблицей рекордов, звуками и кастомными виджетами.

## 🚀 Фичи
- Экранная навигация (`ScreenManager`): имя игрока → меню → категории → игра → лидерборд.
- Сохранение прогресса в `JSON` (локально).
- Лидерборд с подсчётом очков и побед/поражений.
- Звуки кликов и кастомные кнопки с анимациями.
- Аккуратная структура пакета: `screens/`, `game/`, `widgets/`, `utils/`, `assets/`.

## 🖼 Скриншоты / GIF
> _Добавь сюда 2–3 скриншота и короткий GIF работы игры._

## 🧩 Установка и запуск (Desktop)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m word_game_kivy.main
```

## 📱 Сборка под Android (Buildozer)
```bash
# Установи buildozer в Linux/WSL
pip install buildozer cython
buildozer init
# buildozer.spec уже подготовлен в репозитории — проверь названия пакетов
buildozer -v android debug
```
Готовый APK появится в `bin/`.

## 🧪 Тесты
```bash
pytest -q
```

## 🧹 Качество кода
В проекте настроены `ruff`, `black`, `isort` и `pre-commit`:
```bash
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

## 🧭 Структура
```
word_game_kivy/
  assets/
  game/
  screens/
  utils/
  widgets/
  main.py
```

## 🛠 Tech highlights
- Разделённые слои: экраны/логика/виджеты/утилиты.
- Логи через стандартный `logging` (см. `logging_config.py`).
- Защищённое чтение/запись JSON с валидацией (см. `utils/storage.py`).
- Базовые тесты на хранение и сортировку результатов.

## 📍 Roadmap
- [ ] Экран настроек (звук, язык, сложность)
- [ ] i18n (ru/en)
- [ ] Экспорт результатов в CSV
- [ ] Ещё категории/режимы

## 📄 Лицензия
MIT — см. `LICENSE`.