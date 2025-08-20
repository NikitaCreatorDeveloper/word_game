# word_game_kivy/__init__.py
# Шим: даём пакетам короткие имена (screens/utils/game/widgets/sound_manager)
# чтобы старые импорты продолжали работать при запуске как пакет (-m).

import importlib
import os
import sys

_pkg_dir = os.path.dirname(__file__)
# Добавим директорию пакета в sys.path, чтобы `import screens` находился
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

# Пробуем завести алиасы: screens, utils, game, widgets, sound_manager, logging_config
for name in ("screens", "utils", "game", "widgets"):
    try:
        sys.modules.setdefault(name, importlib.import_module(f"word_game_kivy.{name}"))
    except Exception:
        # если подпакета пока нет — просто пропустим
        pass

# Модули верхнего уровня файла
for mod in ("sound_manager", "logging_config"):
    try:
        sys.modules.setdefault(mod, importlib.import_module(f"word_game_kivy.{mod}"))
    except Exception:
        pass
