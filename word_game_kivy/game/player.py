class Player:
    def __init__(self, name):
        self.name = name
        self.won = 0
        self.lost = 0
        self.score = 0
        self.used_words = []  # 👈 Добавлено: список угаданных слов

    def add_win(self):
        self.won += 1
        self.score += 10

    def add_loss(self):
        self.lost += 1

    def add_letter_score(self, count):
        self.score += count

    def remember_word(self, word):
        if word not in self.used_words:
            self.used_words.append(word)
        # 👈 Добавляем слово, если ещё не было

    def to_dict(self):
        return {
            "score": self.score,
            "won": self.won,
            "lost": self.lost,
            "used_words": self.used_words,  # 👈 сохраняем список слов
        }

    @classmethod
    def from_dict(cls, name, data):
        player = cls(name)
        player.score = data.get("score", 0)
        player.won = data.get("won", 0)
        player.lost = data.get("lost", 0)
        player.used_words = data.get("used_words", [])  # 👈 загружаем
        return player
