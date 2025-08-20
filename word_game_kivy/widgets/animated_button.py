from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.button import Button


class AnimatedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_color = kwargs.get("background_color", (0.2, 0.6, 1, 1))
        self.hover_color = tuple(max(c - 0.15, 0) for c in self.original_color[:3]) + (
            1,
        )
        self.pressed_color = tuple(max(c - 0.3, 0) for c in self.original_color[:3]) + (
            1,
        )

        Window.bind(mouse_pos=self.on_mouse_pos)
        self._hovered = False

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

    def on_release(self):
        color = self.hover_color if self._hovered else self.original_color
        self.animate_color(color)

    def animate_color(self, color):
        Animation.cancel_all(self)
        Animation(background_color=color, duration=0.1).start(self)
