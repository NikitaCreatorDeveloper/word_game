# ruff: noqa: E402
from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from .screens.menu_screen import MenuScreen
from .screens.category_screen import CategoryScreen
from .screens.game_screen import GameScreen
from .screens.leaderboard_screen import LeaderboardScreen


class WordGameApp(App):
    title = "Word Game (Kivy)"

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(CategoryScreen(name="category"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(LeaderboardScreen(name="leaderboard"))
        sm.current = "menu"
        return sm


if __name__ == "__main__":
    WordGameApp().run()
