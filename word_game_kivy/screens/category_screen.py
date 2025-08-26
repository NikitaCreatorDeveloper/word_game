from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from ..i18n import t
from ..sound_manager import SOUNDS
from ..game.logic import WORDSETS


class CategoryScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=16, spacing=12)
        root.add_widget(
            Label(
                text=t("choose_category"), font_size="20sp", size_hint_y=None, height=48
            )
        )
        for cat in WORDSETS.keys():
            display = cat.replace("_", " ").title()
            btn = Button(text=display, size_hint_y=None, height=48)
            btn.bind(on_release=lambda *_b, c=cat: self.select_category(c))
            root.add_widget(btn)
        self.add_widget(root)

    def select_category(self, category: str):
        SOUNDS.play("click")
        game = self.manager.get_screen("game")
        game.set_category(category)
        self.manager.current = "game"
