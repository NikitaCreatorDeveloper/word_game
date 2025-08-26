from dataclasses import dataclass, field
from typing import Set
from pathlib import Path
from ..utils import prefs

# attempts by difficulty
MAX_ATTEMPTS_BY_DIFF = {
    "easy": 10,
    "normal": 8,
    "hard": 6,
}

# current values ​​(initialization)
DIFFICULTY = prefs.get_difficulty()
MAX_ATTEMPTS = MAX_ATTEMPTS_BY_DIFF.get(DIFFICULTY, 8)

# WORDSETS will be reloaded from files
WORDSETS: dict[str, list[str]] = {}

WORDS_DIR = Path(__file__).resolve().parents[1] / "words"


def _load_wordsets_for(diff: str) -> dict[str, list[str]]:
    base = WORDS_DIR / diff
    out: dict[str, list[str]] = {}
    if not base.exists():
        return out
    for json_file in base.glob("*.json"):
        try:
            import json

            arr = json.loads(json_file.read_text(encoding="utf-8"))
            # normalize to uppercase and filter
            words = []
            for w in arr:
                w2 = "".join(ch for ch in str(w).strip().upper() if ch.isalpha())
                if 2 <= len(w2) <= 16:
                    words.append(w2)
            if words:
                out[json_file.stem] = words
        except Exception:
            continue
    return out


def set_difficulty(diff: str) -> None:
    """Changes the difficulty globally: attempts and dictionaries."""
    global DIFFICULTY, MAX_ATTEMPTS, WORDSETS
    diff = diff.lower()
    if diff not in ("easy", "normal", "hard"):
        diff = "normal"
    DIFFICULTY = diff
    MAX_ATTEMPTS = MAX_ATTEMPTS_BY_DIFF.get(diff, 8)
    WORDSETS = _load_wordsets_for(diff)


# initial loading when importing a module
WORDSETS = _load_wordsets_for(DIFFICULTY)


@dataclass
class GameState:
    word: str
    guessed: Set[str] = field(default_factory=set)
    wrong: Set[str] = field(default_factory=set)

    def pattern(self) -> str:
        return " ".join(ch if ch in self.guessed else "_" for ch in self.word)

    def is_won(self) -> bool:
        return all(ch in self.guessed for ch in self.word)

    def is_lost(self) -> bool:
        return len(self.wrong) >= MAX_ATTEMPTS

    def guess_letter(self, letter: str) -> str:
        letter = (letter or "").strip().upper()
        if not (len(letter) == 1 and letter.isalpha()):
            return "invalid"
        if letter in self.guessed or letter in self.wrong:
            return "repeat"
        if letter in self.word:
            self.guessed.add(letter)
            return "hit"
        else:
            self.wrong.add(letter)
            return "miss"


def compute_score(word: str, wrong_attempts: int) -> int:
    base = max(10, 120 - 15 * wrong_attempts)
    length_bonus = max(0, len(word) - 4) * 2
    return base + length_bonus
