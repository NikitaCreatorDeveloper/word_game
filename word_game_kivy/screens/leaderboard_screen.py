from kivy.uix.boxlayout import BoxLayout
from screens.base_screen import BaseScreen
from utils.storage import save_players


class LeaderboardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.title_label = self.create_styled_label("Таблица лидеров")
        self.records_label = self.create_styled_label("")
        self.clear_btn = self.create_styled_button("Очистить таблицу")
        self.back_btn = self.create_styled_button("Назад")
        self.back_btn.bind(on_press=self.go_back)  # type: ignore
        self.clear_btn.bind(on_press=self.clear_leaderboard)  # type: ignore

        self.layout.add_widget(self.wrap_centered(self.title_label))
        self.layout.add_widget(self.wrap_centered(self.records_label))
        self.layout.add_widget(self.wrap_centered(self.back_btn))
        self.layout.add_widget(self.wrap_centered(self.clear_btn))
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.update_leaderboard()

    def update_leaderboard(self):
        players = self.manager.players_data
        top_players = sorted(players.values(), key=lambda p: p.score, reverse=True)[:4]
        table_lines = []
        for idx, p in enumerate(top_players, 1):
            line = (
                f"{idx}. {p.name}: {p.score} очков | {p.won} побед | {p.lost} поражений"
            )
            table_lines.append(line)
        self.records_label.text = (
            "\n".join(table_lines) if table_lines else "Нет данных."
        )

    def clear_leaderboard(self, instance):
        self.manager.players_data.clear()
        save_players(self.manager.players_data)
        self.update_leaderboard()

    def go_back(self, instance):
        self.manager.current = "menu"
