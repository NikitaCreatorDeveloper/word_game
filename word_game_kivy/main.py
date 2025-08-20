from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from screens.category_screen import CategoryScreen
from screens.game_screen import GameScreen
from screens.leaderboard_screen import LeaderboardScreen
from screens.menu_screen import MainMenuScreen
from screens.name_screen import NameScreen
from sound_manager import SoundManager

from .logging_config import setup_logging

resource_add_path(str(Path(__file__).resolve().parent))

setup_logging()
with Window.canvas.before:
    Window.bg_rect = Rectangle(
        source="assets/background.jpg",
        pos=(0, 0),  # 👈 фиксированная позиция
        size=Window.size,
    )


def update_bg(*args):
    Window.bg_rect.size = Window.size  # 👈 только размер меняется


Window.bind(size=update_bg)


class WordGameApp(App):
    def build(self):
        self.sound_manager = SoundManager()  # ✅ сначала создаём
        sm = ScreenManager(transition=FadeTransition(duration=0.4))

        game_screen = GameScreen(name="game")
        game_screen.sound_manager = self.sound_manager

        name_screen = NameScreen(name="name")
        name_screen.sound_manager = self.sound_manager

        sm.add_widget(name_screen)
        sm.add_widget(MainMenuScreen(name="menu"))
        sm.add_widget(CategoryScreen(name="category"))
        sm.add_widget(game_screen)
        sm.add_widget(LeaderboardScreen(name="leaderboard"))

        return sm


if __name__ == "__main__":
    WordGameApp().run()
