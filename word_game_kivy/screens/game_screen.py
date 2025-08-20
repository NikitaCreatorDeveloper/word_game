from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from screens.base_screen import BaseScreen
from sound_manager import SoundManager
from utils.storage import save_players


class GameScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound_manager: SoundManager | None = None
        self.layout = BoxLayout(orientation="vertical", padding=30, spacing=15)
        self.word_label = self.create_styled_label("")
        self.info_label = self.create_styled_label("")
        self.attempts_label = self.create_styled_label("")
        self.records_label = self.create_styled_label("")
        self.score_label = self.create_styled_label("")
        self.input = self.create_styled_input(hint_text="Введите букву")
        self.input.multiline = False
        self.submit_btn = self.create_styled_button("Отправить")
        self.submit_btn.bind(on_press=self.submit_letter)  # type: ignore

        Clock.schedule_once(lambda dt: setattr(self.input, "focus", True), 0)

        self.layout.add_widget(self.wrap_centered(self.word_label))
        self.layout.add_widget(self.wrap_centered(self.info_label))
        self.layout.add_widget(self.wrap_centered(self.attempts_label))
        self.layout.add_widget(self.wrap_centered(self.score_label))
        self.layout.add_widget(self.wrap_centered(self.input))
        self.layout.add_widget(self.wrap_centered(self.submit_btn))
        self.layout.add_widget(self.wrap_centered(self.records_label))
        self.add_widget(self.layout)

        self.reset_game_state()

    def reset_game_state(self):
        self.word = ""
        self.display_word = []
        self.attempts_left = 6
        self.guessed_letters = set()
        self.player = None

    def handle_enter(self, instance):
        if self.sound_manager:
            self.sound_manager.play("click")
        self.submit_letter(instance)  # или self.save_name() для NameScreen

    def on_enter(self):
        self.input.focus = True
        self.input.disabled = False
        self.input.bind(on_text_validate=self.handle_enter)  # type: ignore

    def on_leave(self):
        self.input.unbind(on_text_validate=self.handle_enter)  # type: ignore

    def start_game(self, word, player):
        self.input.readonly = False
        self.input.disabled = False
        self.reset_game_state()
        self.word = word.lower()
        self.player = player
        self.display_word = ["_" if c.isalpha() else c for c in self.word]
        self.update_display()
        self.submit_btn.text = "Отправить"
        self.submit_btn.unbind(on_press=self.go_to_menu)  # type: ignore
        self.submit_btn.bind(on_press=self.submit_letter)  # type: ignore

        def refocus_input(*args):
            if not self.input.focus:
                self.input.focus = True

        Clock.schedule_interval(refocus_input, 0)

    def update_display(self):
        self.word_label.text = "Слово: " + " ".join(self.display_word)
        self.attempts_label.text = f"Осталось попыток: {self.attempts_left}"
        if self.player:
            self.score_label.text = f"Очки: {self.player.score}"

    def submit_letter(self, instance=None):
        letter = self.input.text.strip().lower()
        self.input.text = ""

        if not letter or len(letter) != 1 or not letter.isalpha():
            self.info_label.text = "Введите одну букву!"
            Clock.schedule_once(lambda dt: setattr(self.input, "focus", True), 0)
            return

        if letter in self.guessed_letters:
            self.info_label.text = "Вы уже вводили эту букву!"
            Clock.schedule_once(lambda dt: setattr(self.input, "focus", True), 0)
            return

        self.guessed_letters.add(letter)

        if letter in self.word:
            count = self.word.count(letter)
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.display_word[idx] = letter
            count = self.word.count(letter)
            self.info_label.text = f"Буква '{letter}' есть в слове! (+{count} очк.)"
            if self.player:
                self.player.add_letter_score(count)
            Clock.schedule_once(lambda dt: setattr(self.input, "focus", True), 0)
        else:
            self.attempts_left -= 1
            self.info_label.text = (
                f"Буквы '{letter}' нет. Осталось {self.attempts_left} попыток."
            )
            Clock.schedule_once(lambda dt: setattr(self.input, "focus", True), 0)

        self.update_display()

        if "_" not in self.display_word:
            if self.player:
                self.player.add_win()
                self.manager.players_data[self.player.name] = self.player
                save_players(self.manager.players_data)

                Clock.schedule_once(
                    lambda dt: self.manager.sound_manager.play("win"), 0
                )
            self.info_label.text = "Победа! Ты отгадал слово! (+10 очков.)"

            if self.player:
                self.score_label.text = (
                    f"Очки: {self.player.score}"  # 👈 обновляем текст очков
                )

            self.submit_btn.text = "В меню"
            self.submit_btn.unbind(on_press=self.submit_letter)  # type: ignore
            self.submit_btn.bind(on_press=self.go_to_menu)  # type: ignore
            self.input.readonly = True  # 👈 блокируем ввод
            self.input.disabled = True  # 👈 делаем неактивным

        elif self.attempts_left <= 0:
            if self.player:
                self.player.add_loss()
                self.manager.players_data[self.player.name] = self.player
                save_players(self.manager.players_data)

                Clock.schedule_once(
                    lambda dt: self.manager.sound_manager.play("lose"), 0
                )

            self.info_label.text = f"Ты проиграл. Слово было: {self.word}"
            self.submit_btn.text = "В меню"
            self.submit_btn.unbind(on_press=self.submit_letter)  # type: ignore
            self.submit_btn.bind(on_press=self.go_to_menu)  # type: ignore
            self.input.readonly = True
            self.input.disabled = True

    def go_to_menu(self, instance):
        self.records_label.text = ""  # 👈 очищаем таблицу
        self.info_label.text = ""
        self.manager.current = "menu"
