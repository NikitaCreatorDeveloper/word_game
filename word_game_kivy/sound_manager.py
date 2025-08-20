from kivy.core.audio import SoundLoader


class SoundManager:
    def __init__(self):
        self.sounds = {
            "click": SoundLoader.load("assets/sounds/click.wav"),
            "win": SoundLoader.load("assets/sounds/win.wav"),
            "lose": SoundLoader.load("assets/sounds/lose.wav"),
        }

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.stop()  # перезапуск
            sound.play()
        else:
            print(f"Звук '{name}' не найден.")
