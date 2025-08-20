from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from screens.base_screen import BaseScreen


class MainMenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        self.title = self.create_styled_label("Главное меню")
        btn_play = self.create_styled_button("Играть")
        btn_leaderboard = self.create_styled_button("Таблица лидеров")
        btn_exit = self.create_styled_button("Выйти")

        btn_play.bind(on_press=self.go_to_categories)  # type: ignore
        btn_leaderboard.bind(on_press=self.show_leaderboard)  # type: ignore
        btn_exit.bind(on_press=self.exit_game)  # type: ignore

        layout.add_widget(self.wrap_centered(btn_leaderboard))
        layout.add_widget(self.wrap_centered(self.title))
        layout.add_widget(self.wrap_centered(btn_play))
        layout.add_widget(self.wrap_centered(btn_exit))

        self.add_widget(layout)

    def go_to_categories(self, instance):
        self.manager.current = "category"

    def show_leaderboard(self, instance):
        self.manager.current = "leaderboard"

    def exit_game(self, instance):
        from utils.storage import save_players

        save_players(self.manager.players_data)
        app = App.get_running_app()
        if app is not None:
            app.stop()
        else:
            print("Нет запущенного приложения.")
