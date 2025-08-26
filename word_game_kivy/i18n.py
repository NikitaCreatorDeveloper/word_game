LANG = "en"  # set 'ru' for Russian

STRINGS = {
    "en": {
        "title": "Word Game",
        "menu_play": "Play",
        "menu_leaderboard": "Leaderboard",
        "menu_change_player": "Change Player",
        "enter_name": "Enter your name",
        "choose_category": "Choose a category",
        "guess_prompt": "Enter a letter",
        "guessed": "Guessed",
        "wrong": "Wrong",
        "attempts_left": "Attempts left",
        "you_win": "You win!",
        "you_lose": "You lose! The word: ",
        "play_again": "New word",
        "back_menu": "Back to Menu",
        "difficulty": "Difficulty",
        "diff_easy": "Easy",
        "diff_normal": "Normal",
        "diff_hard": "Hard",
        "sfx": "Sound",
        "timer_length": "Timer length",
    },
    "ru": {
        "title": "Игра со словами",
        "menu_play": "Играть",
        "menu_leaderboard": "Лидерборд",
        "menu_change_player": "Сменить игрока",
        "enter_name": "Введите имя",
        "choose_category": "Выберите категорию",
        "guess_prompt": "Введите букву",
        "guessed": "Угадано",
        "wrong": "Ошибки",
        "attempts_left": "Осталось попыток",
        "you_win": "Победа!",
        "you_lose": "Поражение! Слово: ",
        "play_again": "Новое слово",
        "back_menu": "В меню",
        "difficulty": "Сложность",
        "diff_easy": "Лёгкая",
        "diff_normal": "Обычная",
        "diff_hard": "Сложная",
        "sfx": "Звук",
        "timer_length": "Длина таймера",
    },
}


def t(key: str) -> str:
    return STRINGS.get(LANG, STRINGS["en"]).get(key, key)
