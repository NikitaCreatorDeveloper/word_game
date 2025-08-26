from kivy.core.audio import SoundLoader
from .utils.assets import get_asset_path
from .utils import prefs


class SoundManager:
    def __init__(self):
        self._cache = {}

    def load(self, name: str, rel_path: str):
        snd = None
        try:
            path = get_asset_path(rel_path)
            snd = SoundLoader.load(path)
        except Exception:
            snd = None
        self._cache[name] = snd

    def play(self, name: str):
        if not prefs.get_sfx_enabled():
            return
        snd = self._cache.get(name)
        try:
            if snd:
                snd.stop()
                snd.volume = 1.0
                snd.play()
        except Exception:
            pass


SOUNDS = SoundManager()
SOUNDS.load("click", "assets/sounds/click.wav")
SOUNDS.load("win", "assets/sounds/win.wav")
SOUNDS.load("lose", "assets/sounds/lose.wav")
