import pytest

from nyu_wordle.game import WordleGame


def test_single_attempt_win():
    game = WordleGame("apple", max_attempts=1)
    assert game.submit_guess("apple") == "won"
    assert game.get_remaining_attempts() == 0
    assert game.get_guess_history() == ["apple"]


def test_single_attempt_loss():
    game = WordleGame("apple", max_attempts=1)
    assert game.submit_guess("grape") == "lost"
    assert game.get_remaining_attempts() == 0
    assert game.get_status() == "lost"


def test_case_insensitive_secret_and_guess():
    game = WordleGame("ApPlE")
    assert game.secret_word == "apple"
    assert game.submit_guess("APPLE") == "won"
    assert game.get_guess_history() == ["apple"]


def test_mixed_case_wrong_guess_is_normalized():
    game = WordleGame("apple", max_attempts=3)
    assert game.submit_guess("GrApE") == "ongoing"
    assert game.get_guess_history() == ["grape"]
    assert game.get_remaining_attempts() == 2


def test_invalid_guess_does_not_change_state():
    game = WordleGame("apple", max_attempts=2)
    game.submit_guess("grape")
    before = game.get_guess_history()
    with pytest.raises(ValueError):
        game.submit_guess("cat")
    assert game.get_guess_history() == before
    assert game.get_remaining_attempts() == 1
    assert game.get_status() == "ongoing"


@pytest.mark.parametrize("invalid_guess", [None, 12345, ["apple"], {"word": "apple"}])
def test_non_string_guess_does_not_consume_attempt(invalid_guess):
    game = WordleGame("apple")
    with pytest.raises(ValueError):
        game.submit_guess(invalid_guess)
    assert game.get_guess_history() == []
    assert game.get_remaining_attempts() == 6


def test_guess_history_is_defensive_copy():
    game = WordleGame("apple")
    game.submit_guess("grape")
    history = game.get_guess_history()
    history.append("apple")
    assert game.get_guess_history() == ["grape"]
    assert game.get_remaining_attempts() == 5


@pytest.mark.parametrize("winning", [True, False])
def test_no_guesses_allowed_after_game_ends(winning):
    game = WordleGame("apple", max_attempts=1)
    final_status = game.submit_guess("apple" if winning else "grape")
    with pytest.raises(ValueError):
        game.submit_guess("apple")
    assert game.get_status() == final_status
    assert len(game.get_guess_history()) == 1


def test_reset_after_loss_restores_full_attempts():
    game = WordleGame("apple", max_attempts=2)
    game.submit_guess("grape")
    game.submit_guess("melon")
    assert game.get_status() == "lost"
    game.reset_game("MANGO")
    assert game.secret_word == "mango"
    assert game.get_status() == "ongoing"
    assert game.get_remaining_attempts() == 2
    assert game.get_guess_history() == []
    assert game.submit_guess("mango") == "won"


@pytest.mark.parametrize("invalid_secret", [None, "", 12345, ["apple"]])
def test_invalid_initial_secret_rejected(invalid_secret):
    with pytest.raises(ValueError):
        WordleGame(invalid_secret)


@pytest.mark.parametrize("invalid_attempts", [0, -1, 1.5, "6", True, None])
def test_invalid_attempt_limit_rejected(invalid_attempts):
    with pytest.raises(ValueError):
        WordleGame("apple", max_attempts=invalid_attempts)


@pytest.mark.parametrize("invalid_secret", [None, "", 12345, ["apple"]])
def test_invalid_reset_preserves_existing_game(invalid_secret):
    game = WordleGame("apple", max_attempts=3)
    game.submit_guess("grape")
    with pytest.raises(ValueError):
        game.reset_game(invalid_secret)
    assert game.secret_word == "apple"
    assert game.get_guess_history() == ["grape"]
    assert game.get_remaining_attempts() == 2
    assert game.get_status() == "ongoing"
