from kivy.core.audio import SoundLoader


class SoundManager:
    def __init__(self):
        self.sounds = {
            "click": SoundLoader.load("assets/sounds/click.wav"),
            # можешь добавить ещё: "correct", "wrong", "win", "lose"
        }

    def play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.stop()  # перезапуск
            sound.play()
        else:
            print(f"Звук '{name}' не найден.")
