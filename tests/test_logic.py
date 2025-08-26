from word_game_kivy.game.logic import GameState


def test_letter_flow():
    s = GameState("KIVY")
    assert s.guess_letter("K") == "hit"
    assert s.guess_letter("Z") == "miss"
    for ch in "IVY":
        s.guess_letter(ch)
    assert s.is_won()
