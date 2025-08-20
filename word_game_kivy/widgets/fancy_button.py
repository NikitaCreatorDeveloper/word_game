from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button


class FancyButton(Button):
    def __init__(self, sound_path=None, **kwargs):
        super().__init__(**kwargs)

        # Цвета
        self.original_color = kwargs.get("background_color", (0.2, 0.6, 1, 1))
        self.hover_color = tuple(max(c - 0.1, 0) for c in self.original_color[:3]) + (
            0.9,
        )
        self.pressed_color = tuple(max(c - 0.2, 0) for c in self.original_color[:3]) + (
            0.95,
        )

        # Тень
        with self.canvas.before:  # type: ignore
            Color(0, 0, 0, 0.3)
            self.shadow = RoundedRectangle(
                pos=(self.x + 4, self.y - 4),
                size=(self.width + 4, self.height + 4),
                radius=[2],
            )

        self.bind(pos=self.update_shadow, size=self.update_shadow)  # type: ignore

        # Наведение
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._hovered = False

        # Звук
        self.click_sound = SoundLoader.load(sound_path) if sound_path else None

    def update_shadow(self, *args):
        self.shadow.pos = (self.x + 2, self.y - 4)
        self.shadow.size = (self.width + 2, self.height + 0)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        inside = self.collide_point(*self.to_widget(*pos))
        if inside and not self._hovered:
            self._hovered = True
            self.animate_color(self.hover_color)
        elif not inside and self._hovered:
            self._hovered = False
            self.animate_color(self.original_color)

    def on_press(self):
        self.animate_color(self.pressed_color)
        if self.click_sound:
            self.click_sound.stop()
            self.click_sound.play()

    def on_release(self):
        color = self.hover_color if self._hovered else self.original_color
        self.animate_color(color)

    def animate_color(self, color):
        Animation.cancel_all(self)
        Animation(background_color=color, duration=0.1).start(self)
