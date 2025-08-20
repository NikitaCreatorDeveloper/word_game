from functools import partial

from kivy.uix.boxlayout import BoxLayout
from screens.base_screen import BaseScreen


class CategoryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.books = ["marlin", "friends", "harry", "hobbit"]
        self.movies = ["matrix", "inception", "avatar", "tenet"]
        self.holy = ["grace", "prayer", "faith", "repentance"]

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        label = self.create_styled_label("Выберите категорию")

        btn_books = self.create_styled_button("Книги")
        btn_movies = self.create_styled_button("Фильмы")
        btn_holy = self.create_styled_button("Вера")
        btn_back = self.create_styled_button("Назад")

        btn_books.bind(on_press=lambda x: self.start_game(self.books))  # type: ignore
        btn_movies.bind(on_press=lambda x: self.start_game(self.movies))  # type: ignore
        btn_holy.bind(on_press=lambda x: self.start_game(self.holy))  # type: ignore
        btn_back.bind(on_press=partial(self.switch_screen, "menu"))  # type: ignore

        layout.add_widget(self.wrap_centered(label))
        layout.add_widget(self.wrap_centered(btn_books))
        layout.add_widget(self.wrap_centered(btn_movies))
        layout.add_widget(self.wrap_centered(btn_holy))
        layout.add_widget(self.wrap_centered(btn_back))

        self.add_widget(layout)

    def switch_screen(self, screen_name, *args):
        self.manager.current = screen_name

    def start_game(self, word_list):
        import random

        player = self.manager.current_player

        # Исключаем использованные слова
        available_words = [w for w in word_list if w not in player.used_words]
        if not available_words:
            player.used_words.clear()
            available_words = word_list[:]

        word = random.choice(available_words)
        player.remember_word(word)

        game_screen = self.manager.get_screen("game")
        game_screen.start_game(word, player)
        self.manager.current = "game"
