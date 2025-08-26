import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.animation import Animation
from ..i18n import t
from ..game import logic
from ..game.logic import GameState, compute_score
from ..utils.storage import DATA_DIR, load_json, save_json
from ..utils import prefs
from ..game.player import Player
from ..sound_manager import SOUNDS

PLAYERS_PATH = DATA_DIR / "players.json"
PROFILE_PATH = DATA_DIR / "profile.json"


def _get_profile_name() -> str:
    return load_json(PROFILE_PATH, {}).get("player_name", "Player")


def _load_players() -> dict:
    return load_json(PLAYERS_PATH, {})


def _save_players(data: dict) -> None:
    save_json(PLAYERS_PATH, data)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = None
        self.state: GameState | None = None

        # Basic Layout
        self.layout = BoxLayout(orientation="vertical", padding=12, spacing=8)

        # Messages (Win / Lose / Hints) - Top
        self.lbl_message = Label(
            text="",
            size_hint_y=None,
            height=40,
            font_size="24sp",
            halign="center",
        )
        self.lbl_message.bind(
            size=lambda *_: setattr(
                self.lbl_message, "text_size", (self.lbl_message.width, None)
            )
        )

        # Timer (under the message)
        self.lbl_timer = Label(
            text="",
            size_hint_y=None,
            height=24,
            halign="center",
        )
        self.lbl_timer.bind(
            size=lambda *_: setattr(
                self.lbl_timer, "text_size", (self.lbl_timer.width, None)
            )
        )

        # Word - centered (via AnchorLayout)
        self.lbl_word = Label(
            text="",
            font_size="42sp",
            size_hint_y=None,
            height=72,
            halign="center",
        )
        self.lbl_word.bind(
            size=lambda *_: setattr(
                self.lbl_word, "text_size", (self.lbl_word.width, None)
            )
        )
        mid = AnchorLayout(anchor_y="center", size_hint_y=1)
        mid.add_widget(self.lbl_word)

        # Information and statistics
        self.lbl_info = Label(text="", size_hint_y=None, height=24)
        self.lbl_stats = Label(text="", size_hint_y=None, height=24)

        # Input field + "Guess" button
        row = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=44, spacing=6
        )
        self.input = TextInput(multiline=False, hint_text=t("guess_prompt"))
        self.input.input_filter = self._letters_only
        self.input.write_tab = False
        self.input.bind(text=lambda inst, val: setattr(inst, "text", val.upper()))
        self.input.focus = True
        self.btn_guess = Button(text="Guess")
        row.add_widget(self.input)
        row.add_widget(self.btn_guess)

        # Control buttons (New word / Menu)
        ctrl = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=44, spacing=6
        )
        self.btn_new = Button(text=t("play_again"))
        self.btn_menu = Button(text=t("back_menu"))
        ctrl.add_widget(self.btn_new)
        ctrl.add_widget(self.btn_menu)

        # Add everything to the layout (correct order)
        self.layout.add_widget(self.lbl_message)
        self.layout.add_widget(self.lbl_timer)
        self.layout.add_widget(mid)
        self.layout.add_widget(self.lbl_info)
        self.layout.add_widget(self.lbl_stats)
        self.layout.add_widget(row)
        self.layout.add_widget(ctrl)

        self.add_widget(self.layout)

        self._apply_theme_and_scale()

        # Official
        self.game_over = False

        # Event Bindings
        self.btn_guess.bind(on_release=lambda *_: self._on_submit())
        self.input.bind(on_text_validate=lambda *_: self._on_submit())  # ENTER
        self.btn_new.bind(on_release=self._on_new_word_btn)
        self.btn_menu.bind(on_release=lambda *_: self._go_menu())

    def _apply_theme_and_scale(self):
        theme = prefs.get_theme()
        if theme == "light":
            Window.clearcolor = (1, 1, 1, 1)
            fg = (0, 0, 0, 1)
        else:
            Window.clearcolor = (0.08, 0.08, 0.1, 1)
            fg = (1, 1, 1, 1)
        for lbl in (
            self.lbl_message,
            self.lbl_word,
            self.lbl_info,
            self.lbl_stats,
            self.lbl_timer,
        ):
            try:
                lbl.color = fg
            except Exception:
                pass
        try:
            s = float(prefs.get_font_scale())
            self.lbl_message.font_size = f"{int(24*s)}sp"
            self.lbl_word.font_size = f"{int(42*s)}sp"
        except Exception:
            pass

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 27:  # ESC
            self._go_menu()
            return True
        if "ctrl" in modifiers and (codepoint in ("n", "N") or key == 110):
            self._on_new_word_btn()
            return True
        return False

    def on_leave(self, *args):
        # remove only if they were attached
        if getattr(self, "_kb_bound", False):
            try:
                Window.unbind(on_key_down=self._on_key_down)
            except Exception:
                pass
            self._kb_bound = False
        # stop the timer if you use it
        self._cancel_timer()

    def _on_new_word_btn(self, *_):
        SOUNDS.play("click")
        self._new_word()

    def _focus_next_tick(self):
        Clock.schedule_once(lambda *_: setattr(self.input, "focus", True), 0)

    def _set_active(self, active: bool):
        # enables/disables input and button
        self.input.disabled = not active
        self.btn_guess.disabled = not active
        if active:
            self._focus_next_tick()  # return focus on activation

    def _add_score(self, delta: int):
        if delta <= 0:
            return
        name = _get_profile_name()
        data = _load_players()
        rec = data.get(name) or Player(name=name).to_dict()
        rec["score"] = rec.get("score", 0) + delta
        data[name] = rec
        _save_players(data)
        self._refresh_ui()

    def on_pre_enter(self, *args):
        self._focus_next_tick()

    def on_enter(self, *args):
        self._focus_next_tick()
        if not getattr(self, "_kb_bound", False):
            Window.bind(on_key_down=self._on_key_down)
            self._kb_bound = True

    def _letters_only(self, substring, from_undo):
        return "".join(ch for ch in substring if ch.isalpha())

    def set_category(self, category: str):
        self.category = category
        self._new_word()

    def _new_word(self):
        words = logic.WORDSETS.get(self.category or "", [])
        word = random.choice(words) if words else "KIVY"
        self.state = GameState(word=word)
        self._set_message("")
        self.lbl_message.color = (
            (1, 1, 1, 1) if prefs.get_theme() == "dark" else (0, 0, 0, 1)
        )
        self.lbl_word.opacity = 1.0
        self._refresh_ui()
        self._focus_next_tick()
        self.game_over = False
        self._set_active(True)
        self._start_timer()

    def _refresh_ui(self):
        s = self.state
        if not s:
            return
        self.lbl_word.text = s.pattern()
        attempts_left = max(0, logic.MAX_ATTEMPTS - len(s.wrong))
        wrong_letters = [x for x in s.wrong if x.isalpha()]
        self.lbl_info.text = (
            f"{t('guessed')}: {' '.join(sorted(s.guessed))} | "
            f"{t('wrong')}: {' '.join(sorted(wrong_letters))} | "
            f"{t('attempts_left')}: {attempts_left}"
        )
        name = _get_profile_name()
        p = _load_players().get(
            name, {"name": name, "wins": 0, "losses": 0, "score": 0}
        )
        self.lbl_stats.text = (
            f"{name} — Score: {p['score']} | W: {p['wins']} | L: {p['losses']}"
        )

    def _set_message(self, msg: str):
        self.lbl_message.text = msg or ""

    def _blink_word(self, times: int = 3, duration: float = 0.2):
        """
        Simple word blink: opacity 1 -> 0 -> 1, repeat N times.
        times: how many times to blink
        duration: total duration of one cycle (there+back)
        """
        if times <= 0:
            return

        # One cycle: extinguish and light
        half = duration / 2.0
        anim = Animation(opacity=0.0, duration=half) + Animation(
            opacity=1.0, duration=half
        )

        # After the loop is complete, repeat recursively (times-1)
        def _again(*_):
            self._blink_word(times=times - 1, duration=duration)

        anim.bind(on_complete=_again)
        anim.start(self.lbl_word)

        # === GAME INPUT / FLOW ===

    def _on_submit(self):
        if self.game_over:
            self._set_message('Round ended. Press "New word".')
            return

        s = self.state
        if not s:
            self._focus_next_tick()
            return

        text = (self.input.text or "").strip().upper()
        self.input.text = ""
        if not text:
            self._focus_next_tick()
            return

        # Guess whole word
        if len(text) > 1:
            if text == s.word:
                for ch in set(s.word):
                    s.guessed.add(ch)
                self._handle_win()
            else:
                s.wrong.add(f"#{len(s.wrong)+1}")
                self._set_message("Wrong word — try letters or another word.")
                if s.is_lost():
                    self._handle_lose()
                else:
                    SOUNDS.play("click")
                    self._refresh_ui()
            self._focus_next_tick()
            return

        # Guess single letter
        res = s.guess_letter(text)
        if res == "invalid":
            self._set_message("Please enter a letter A–Z.")
            self._focus_next_tick()
            return
        if res == "repeat":
            self._set_message("Already tried that.")
            SOUNDS.play("click")
            self._focus_next_tick()
            return
        elif res == "hit":
            bonus = prefs.get_letter_bonus()
            self._add_score(bonus)
            self._set_message(f"Nice! +{bonus}")
            SOUNDS.play("click")
        else:
            self._set_message("No such letter.")
            SOUNDS.play("click")

        if s.is_won():
            self._handle_win()
        elif s.is_lost():
            self._handle_lose()
        else:
            self._refresh_ui()
        self._focus_next_tick()

    def _handle_win(self):
        s = self.state
        pts = compute_score(s.word, len(s.wrong))
        self._apply_result(win=True, score_delta=pts)
        SOUNDS.play("win")
        self._refresh_ui()

        self.lbl_message.color = (0, 1, 0, 1)
        self._set_message(t("you_win") + f" (+{pts})")
        self.lbl_word.text = " ".join(list(s.word))
        self._blink_word(times=3, duration=0.18)

        self.game_over = True
        self._set_active(False)

    def _handle_lose(self):
        s = self.state
        self._apply_result(win=False, score_delta=0)
        SOUNDS.play("lose")
        self._refresh_ui()

        self.lbl_message.color = (1, 0.2, 0.2, 1)
        self._set_message(f"{t('you_lose')}: {s.word}")
        self.lbl_word.text = " ".join(list(s.word))
        self._blink_word(times=4, duration=0.15)

        self.game_over = True
        self._set_active(False)

    def _apply_result(self, win: bool, score_delta: int):
        name = _get_profile_name()
        data = _load_players()
        rec = data.get(name) or Player(name=name).to_dict()
        if win:
            rec["wins"] = rec.get("wins", 0) + 1
            rec["score"] = rec.get("score", 0) + score_delta
        else:
            rec["losses"] = rec.get("losses", 0) + 1
        data[name] = rec
        _save_players(data)

    def _go_menu(self):
        SOUNDS.play("click")
        self.manager.current = "menu"

    # === TIMER API ===
    def _start_timer(self):
        # if the timer is off - just clear the line and exit
        if not prefs.get_timer_enabled():
            self.lbl_timer.text = ""
            self._cancel_timer()
            return
        # start again
        self._cancel_timer()
        self._time_left = int(prefs.get_timer_seconds())
        self._update_timer_label()
        from kivy.clock import Clock

        self._timer_ev = Clock.schedule_interval(self._tick_timer, 1.0)

    def _cancel_timer(self):
        ev = getattr(self, "_timer_ev", None)
        if ev is not None:
            try:
                ev.cancel()
            except Exception:
                pass
        self._timer_ev = None

    def _tick_timer(self, dt=0):
        if self.game_over:
            self._cancel_timer()
            return
        self._time_left -= 1
        if self._time_left <= 0:
            self._cancel_timer()
            if self.state and not self.state.is_won():
                self._handle_lose()
        else:
            self._update_timer_label()

    def _update_timer_label(self):
        m = int(self._time_left) // 60
        s = int(self._time_left) % 60
        self.lbl_timer.text = f"⏱ {m:02d}:{s:02d}"
