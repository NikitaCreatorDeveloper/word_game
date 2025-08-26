from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from ..utils.storage import DATA_DIR, load_json, save_json
from ..sound_manager import SOUNDS

PLAYERS_PATH = DATA_DIR / "players.json"


def load_players_sorted() -> list[dict]:
    data = load_json(PLAYERS_PATH, {})
    players = list(data.values())
    # Сортируем: score ↓, wins ↓, name ↑
    players.sort(
        key=lambda p: (-p.get("score", 0), -p.get("wins", 0), p.get("name", ""))
    )
    return players


class LeaderboardScreen(Screen):
    def on_pre_enter(self):
        self._render()

    def _render(self):
        self.clear_widgets()

        root = BoxLayout(orientation="vertical", padding=12, spacing=8)

        # Заголовок таблицы
        header = GridLayout(cols=4, size_hint_y=None, height=32, spacing=4)
        header.add_widget(Label(text="[b]Name[/b]", markup=True))
        header.add_widget(Label(text="[b]Score[/b]", markup=True))
        header.add_widget(Label(text="[b]Wins[/b]", markup=True))
        header.add_widget(Label(text="[b]Losses[/b]", markup=True))
        root.add_widget(header)

        players = load_players_sorted()

        if not players:
            root.add_widget(
                Label(
                    text="No records yet — play a round!", size_hint_y=None, height=28
                )
            )
        else:
            scroll = ScrollView(size_hint=(1, 1))
            table = GridLayout(
                cols=4,
                size_hint_y=None,
                row_default_height=28,
                spacing=4,
                padding=[0, 0, 10, 0],
            )
            table.bind(minimum_height=table.setter("height"))

            for p in players:
                table.add_widget(Label(text=str(p.get("name", ""))))
                table.add_widget(Label(text=str(p.get("score", 0))))
                table.add_widget(Label(text=str(p.get("wins", 0))))
                table.add_widget(Label(text=str(p.get("losses", 0))))

            scroll.add_widget(table)
            root.add_widget(scroll)

        # Кнопки управления
        btns = BoxLayout(size_hint_y=None, height=44, spacing=8)
        back_btn = Button(text="Back")
        clear_btn = Button(text="Clear Leaderboard")
        back_btn.bind(on_release=lambda *_: self._back())
        clear_btn.bind(on_release=lambda *_: self._clear())
        btns.add_widget(back_btn)
        btns.add_widget(clear_btn)
        root.add_widget(btns)

        self.add_widget(root)

    def _back(self):
        SOUNDS.play("click")
        self.manager.current = "menu"

    def _clear(self):
        SOUNDS.play("click")
        save_json(PLAYERS_PATH, {})  # очистили файл
        self._render()  # перерисовали экран
