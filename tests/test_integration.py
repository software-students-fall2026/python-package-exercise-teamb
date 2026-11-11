import pytest

from nyu_wordle.val import val_try, clean
from nyu_wordle.check_guess import check_guess
from nyu_wordle.game import WordleGame



VOCABULARY = {"apple", "grape", "melon", "peach", "berry"}


def play_guess(game, raw_guess):
    """Model how a caller coordinates the package's three components."""
    valid, message = val_try(raw_guess, word_list=VOCABULARY)
    if not valid:
        return {"valid": False, "message": message}

    guess = clean(raw_guess)
    feedback = check_guess(guess, game.secret_word)
    status = game.submit_guess(guess)
    return {"valid": True, "feedback": feedback, "status": status}


def test_complete_game_win():
    game = WordleGame("apple")
    first = play_guess(game, "grape")
    assert first["valid"] is True
    assert first["status"] == "ongoing"
    assert first["feedback"] == ["absent", "absent", "present", "present", "correct"]

    winning = play_guess(game, " APPLE ")
    assert winning["valid"] is True
    assert winning["feedback"] == ["correct"] * 5
    assert winning["status"] == "won"
    assert game.get_guess_history() == ["grape", "apple"]
    assert game.get_remaining_attempts() == 4


def test_complete_game_loss():
    game = WordleGame("apple", max_attempts=2)
    assert play_guess(game, "grape")["status"] == "ongoing"
    assert play_guess(game, "melon")["status"] == "lost"
    assert game.get_status() == "lost"
    assert game.get_remaining_attempts() == 0
    assert game.get_guess_history() == ["grape", "melon"]
    with pytest.raises(ValueError, match="already ended"):
        play_guess(game, "apple")


@pytest.mark.parametrize("invalid", ["", "cat", "12345", "zzzzz", "gr@pe"])
def test_invalid_guess_does_not_consume_attempt(invalid):
    game = WordleGame("apple")
    result = play_guess(game, invalid)
    assert result["valid"] is False
    assert result["message"]
    assert game.get_remaining_attempts() == 6
    assert game.get_guess_history() == []
    assert game.get_status() == "ongoing"


def test_reset_after_loss_then_win():
    game = WordleGame("apple", max_attempts=1)
    assert play_guess(game, "grape")["status"] == "lost"
    game.reset_game("melon")
    assert game.get_status() == "ongoing"
    assert game.get_remaining_attempts() == 1
    assert game.get_guess_history() == []
    assert play_guess(game, "melon")["status"] == "won"


def test_duplicate_letter_feedback_with_game_state():
    game = WordleGame("apple")
    result = play_guess(game, "peach")
    assert result["valid"] is True
    assert result["feedback"] == ["present", "present", "present", "absent", "absent"]
    assert result["status"] == "ongoing"
    assert game.get_guess_history() == ["peach"]
