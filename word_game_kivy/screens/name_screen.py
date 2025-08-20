from game.player import Player
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from screens.base_screen import BaseScreen
from sound_manager import SoundManager
from utils.storage import load_players


class NameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound_manager: SoundManager | None = None
        self.layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.label = self.create_styled_label("Введите ваше имя:")

        self.name_input = self.create_styled_input()
        self.name_input.multiline = False

        self.button = self.create_styled_button("Продолжить")
        self.button.bind(on_press=self.save_name)  # type: ignore

        self.layout.add_widget(self.wrap_centered(self.label))
        self.layout.add_widget(self.wrap_centered(self.name_input))
        self.layout.add_widget(self.wrap_centered(self.button))

        self.add_widget(self.layout)

        def refocus_input(dt):
            if not self.name_input.focus:
                self.name_input.focus = True

        Clock.schedule_interval(refocus_input, 0)

    def on_pre_enter(self):
        # Устанавливаем фокус через Clock, чтобы сработало после рендеринга
        Clock.schedule_once(lambda dt: setattr(self.name_input, "focus", True), 0)

    def handle_enter(self, instance):
        if self.sound_manager:
            self.sound_manager.play("click")
        self.save_name(instance)

    def on_enter(self):
        self.name_input.focus = True
        self.name_input.bind(on_text_validate=self.handle_enter)  # type: ignore

    def on_leave(self):
        self.name_input.unbind(on_text_validate=self.handle_enter)  # type: ignore

    def save_name(self, instance=None):
        if self.sound_manager:
            self.sound_manager.play("click")

        name = self.name_input.text.strip()
        if not name:
            self.label.text = "Введите имя!"
            return

        players = load_players()

        if name not in players:
            players[name] = Player(name)

        self.manager.current = "menu"
        self.manager.current_player = players[name]
        self.manager.players_data = players
