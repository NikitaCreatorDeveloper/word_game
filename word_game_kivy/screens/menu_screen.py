from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from ..i18n import t
from ..utils import prefs
from ..utils.storage import DATA_DIR, load_json, save_json
from ..sound_manager import SOUNDS

PROFILE_PATH = DATA_DIR / "profile.json"


def get_player_name() -> str:
    data = load_json(PROFILE_PATH, {})
    return data.get("player_name", "")


def set_player_name(name: str) -> None:
    data = load_json(PROFILE_PATH, {})
    data["player_name"] = name.strip()
    save_json(PROFILE_PATH, data)


class MenuScreen(Screen):
    def on_pre_enter(self):
        # Ensure player name exists
        if not get_player_name():
            self.open_name_popup()

        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=16, spacing=12)
        title = Label(text=t("title"), font_size="24sp", size_hint_y=None, height=48)
        btn_play = Button(
            text=t("menu_play"),
            size_hint_y=None,
            height=48,
            on_release=lambda *_: self.start_game(),
        )
        btn_lb = Button(
            text=t("menu_leaderboard"),
            size_hint_y=None,
            height=48,
            on_release=lambda *_: self.open_leaderboard(),
        )
        btn_change = Button(
            text=t("menu_change_player"),
            size_hint_y=None,
            height=48,
            on_release=lambda *_: (SOUNDS.play("click"), self.open_name_popup()),
        )
        root.add_widget(title)
        root.add_widget(btn_play)
        root.add_widget(btn_lb)
        root.add_widget(btn_change)

        # Settings button
        btn_settings = Button(text=t("Settings"), size_hint_y=None, height=48)
        btn_settings.bind(
            on_release=lambda *_: (SOUNDS.play("click"), self.open_settings_popup())
        )

        root.add_widget(btn_settings)
        self.add_widget(root)

    def start_game(self):
        SOUNDS.play("click")
        self.manager.current = "category"

    def open_leaderboard(self):
        SOUNDS.play("click")
        self.manager.current = "leaderboard"

    def open_name_popup(self):
        layout = BoxLayout(orientation="vertical", padding=12, spacing=8)

        ti = TextInput(
            text=get_player_name(),
            multiline=False,
            hint_text=t("enter_name"),
        )
        ok_btn = Button(text="OK", size_hint_y=None, height=44)

        layout.add_widget(ti)
        layout.add_widget(ok_btn)

        popup = Popup(
            title=t("enter_name"),
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
        )

        def _save_and_close(*_):
            SOUNDS.play("click")
            name = ti.text.strip() or "Player"
            set_player_name(name)
            popup.dismiss()

        # confirmation Enter
        ti.bind(on_text_validate=_save_and_close)
        # focus immediately in the field
        ti.focus = True

        # (optional) highlight text when receiving focus - handy for instantly replacing a name
        def _select_all(_inst, focused):
            if focused:
                ti.select_all()

        ti.bind(focus=_select_all)

        ok_btn.bind(on_release=_save_and_close)
        popup.open()

    def open_settings_popup(self):
        # === ROOT: vertical scrolling container + footer ===
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)

        scroll = ScrollView(size_hint=(1, 1))
        inner = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))
        scroll.add_widget(inner)

        # === ТЕМА ===
        current_theme = prefs.get_theme()
        btn_theme = Button(
            text=f"{t('theme')}: {t('theme_light') if current_theme=='light' else t('theme_dark')}",
            size_hint_y=None,
            height=44,
        )

        def _toggle_theme(*_):
            SOUNDS.play("click")
            new_theme = "dark" if prefs.get_theme() == "light" else "light"
            prefs.set_theme(new_theme)
            btn_theme.text = f"{t('theme')}: {t('theme_light') if new_theme=='light' else t('theme_dark')}"
            # instantly apply to all screens

            Window.clearcolor = (
                (1, 1, 1, 1) if new_theme == "light" else (0.08, 0.08, 0.1, 1)
            )
            if self.manager:
                for scr in self.manager.screens:
                    if hasattr(scr, "_apply_theme_and_scale"):
                        scr._apply_theme_and_scale()

        btn_theme.bind(on_release=_toggle_theme)
        inner.add_widget(btn_theme)

        # === FONT SCALE ===
        fs = prefs.get_font_scale()
        lbl_fs = Label(text=f"{t('font_scale')}: {fs}x", size_hint_y=None, height=28)
        inner.add_widget(lbl_fs)

        row_fs = BoxLayout(
            orientation="horizontal", spacing=6, size_hint_y=None, height=44
        )
        for s in (1.0, 1.25, 1.5):
            b = Button(text=f"{s}x")

            def handler(btn, val=s):
                SOUNDS.play("click")
                prefs.set_font_scale(val)
                lbl_fs.text = f"{t('font_scale')}: {val}x"
                if self.manager:
                    for scr in self.manager.screens:
                        if hasattr(scr, "_apply_theme_and_scale"):
                            scr._apply_theme_and_scale()

            b.bind(on_release=handler)
            row_fs.add_widget(b)
        inner.add_widget(row_fs)

        # === TIMER: ON/OFF ===
        tm = prefs.get_timer_enabled()
        btn_timer = Button(
            text=f"{t('timer_mode')}: {t('enabled') if tm else t('disabled')}",
            size_hint_y=None,
            height=44,
        )

        def _toggle_timer(*_):
            SOUNDS.play("click")
            prefs.set_timer_enabled(not prefs.get_timer_enabled())
            btn_timer.text = f"{t('timer_mode')}: {t('enabled') if prefs.get_timer_enabled() else t('disabled')}"

        btn_timer.bind(on_release=_toggle_timer)
        inner.add_widget(btn_timer)

        # === DIFFICULTY ===
        def _diff_title(d):
            return {
                "easy": t("diff_easy"),
                "normal": t("diff_normal"),
                "hard": t("diff_hard"),
            }.get(d, t("diff_normal"))

        cur_diff = prefs.get_difficulty()
        btn_diff = Button(
            text=f"{t('difficulty')}: {_diff_title(cur_diff)}",
            size_hint_y=None,
            height=44,
        )

        def _cycle_diff(*_):
            SOUNDS.play("click")
            order = ["easy", "normal", "hard"]
            d = prefs.get_difficulty()
            nxt = order[(order.index(d) + 1) % len(order)] if d in order else "normal"
            prefs.set_difficulty(nxt)
            # toggle complexity in logic to update WORDSETS and MAX_ATTEMPTS
            from ..game import logic

            logic.set_difficulty(nxt)
            btn_diff.text = f"{t('difficulty')}: {_diff_title(nxt)}"
            # refresh the categories screen if it is already live
            if self.manager and self.manager.has_screen("category"):
                cat = self.manager.get_screen("category")
                if hasattr(cat, "on_pre_enter"):
                    cat.on_pre_enter()

        btn_diff.bind(on_release=_cycle_diff)
        inner.add_widget(btn_diff)

        # === SOUND (SFX) ===
        cur_sfx = prefs.get_sfx_enabled()
        btn_sfx = Button(
            text=f"{t('sfx')}: {t('enabled') if cur_sfx else t('disabled')}",
            size_hint_y=None,
            height=44,
        )

        def _toggle_sfx(*_):
            SOUNDS.play("click")
            val = not prefs.get_sfx_enabled()
            prefs.set_sfx_enabled(val)
            btn_sfx.text = f"{t('sfx')}: {t('enabled') if val else t('disabled')}"

        btn_sfx.bind(on_release=_toggle_sfx)
        inner.add_widget(btn_sfx)

        # === TIMER LENGTH (PRESETS) ===
        lbl_timer_len = Label(
            text=f"{t('timer_length')}: {prefs.get_timer_seconds()}s",
            size_hint_y=None,
            height=28,
        )
        inner.add_widget(lbl_timer_len)

        row_timer = BoxLayout(
            orientation="horizontal", spacing=6, size_hint_y=None, height=44
        )
        for sec in (30, 60, 90, 120):
            b = Button(text=f"{sec}s")

            def _set_len(btn, val=sec):
                SOUNDS.play("click")
                prefs.set_timer_seconds(val)
                lbl_timer_len.text = f"{t('timer_length')}: {val}s"

            b.bind(on_release=_set_len)
            row_timer.add_widget(b)
        inner.add_widget(row_timer)

        # === Footer: OK ===
        footer = BoxLayout(orientation="horizontal", size_hint_y=None, height=48)
        ok_btn = Button(text="OK")
        ok_btn.bind(on_release=lambda *_: (SOUNDS.play("click"), popup.dismiss()))
        footer.add_widget(ok_btn)

        # collect popup
        root.add_widget(scroll)
        root.add_widget(footer)

        popup = Popup(
            title=t("Settings"),
            content=root,
            size_hint=(0.8, 0.8),
            auto_dismiss=False,
        )
        # === we use integer font size in popup to avoid blur ===
        scale = float(prefs.get_font_scale())

        def _apply_popup_font_sizes():
            fs_btn = int(16 * scale)
            fs_lbl = int(14 * scale)

            # single widgets
            for w in (
                btn_theme,
                lbl_fs,
                btn_timer,
                btn_diff,
                btn_sfx,
                lbl_timer_len,
                ok_btn,
            ):
                if hasattr(w, "font_size"):
                    w.font_size = (
                        f"{fs_btn if w.__class__.__name__=='Button' else fs_lbl}sp"
                    )

            # buttons in rows
            for row in (row_fs, row_timer):
                for w in getattr(row, "children", []):
                    if hasattr(w, "font_size"):
                        w.font_size = f"{fs_btn}sp"

        _apply_popup_font_sizes()

        popup.open()
