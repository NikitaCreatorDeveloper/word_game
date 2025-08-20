from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from widgets.fancy_button import FancyButton


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_background)

    def add_background(self, dt):
        with self.canvas.before:  # type: ignore
            self.bg_rect = Rectangle(
                source="assets/background.png", pos=self.pos, size=self.size
            )
        self.bind(pos=self.update_bg, size=self.update_bg)  # type: ignore

    def update_bg(self, *args):
        if hasattr(self, "bg_rect"):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size

    def wrap_centered(self, widget):
        wrapper = AnchorLayout(anchor_x="center", anchor_y="center")
        wrapper.add_widget(widget)
        return wrapper

    # 🎨 Стилизация по умолчанию

    def create_styled_button(self, text, **kwargs):
        return FancyButton(
            text=text,
            font_size=26,
            font_name="assets/fonts/roboto_bold.ttf",
            color=(1, 1, 1, 1),
            size_hint=(0.5, 0.8),
            background_normal="",
            # background_down="assets/btn_bg_pressed.png",
            background_color=(0.2, 0.6, 1, 0.85),
            sound_path="assets/sounds/click.wav",
            **kwargs,
        )

    def create_styled_label(self, text="", **kwargs):
        return Label(
            text=text,
            size_hint=(1, 0.1),
            font_size=38,
            font_name="assets/fonts/roboto_bold.ttf",
            color=(0.1, 0.3, 0.6, 1),
            **kwargs,
        )

    def create_styled_input(self, **kwargs):
        return TextInput(
            size_hint=(0.7, 0.7),
            multiline=False,
            font_size=32,
            font_name="assets/fonts/roboto_bold.ttf",
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.1, 0.3, 0.6, 1),
            cursor_color=(0.2, 0.6, 1, 1),
            **kwargs,
        )
