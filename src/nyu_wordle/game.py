from collections.abc import Iterable
import random

class WordleGame:
    def __init__(self, secret_word, max_attempts=6):
        if not isinstance(secret_word, str) or not secret_word:
            raise ValueError("Secret word must be a non-empty string")

        if type(max_attempts) is not int or max_attempts < 1:
            raise ValueError("Maximum attempts must be a positive integer")

        self.secret_word = secret_word.lower()
        self.max_attempts = max_attempts
        self.guesses = []
        self.status = "ongoing"

    def choose_random_word(word_list: Iterable[str]) -> str:
        return random.choice(word_list)

    def submit_guess(self, guess):
        """Record a validated guess and update the game state."""
        if self.status != "ongoing":
            raise ValueError("The game has already ended")

        if not isinstance(guess, str):
            raise ValueError("Guess must be a string")

        guess = guess.lower()

        if len(guess) != len(self.secret_word):
            raise ValueError("Incorrect guess length")

        # Dictionary validation is handled by a teammate.
        self.guesses.append(guess)

        if guess == self.secret_word:
            self.status = "won"
        elif len(self.guesses) >= self.max_attempts:
            self.status = "lost"

        return self.status

    def get_remaining_attempts(self):
        """Return the number of remaining guesses."""
        return self.max_attempts - len(self.guesses)

    def get_status(self):
        """Return ongoing, won, or lost."""
        return self.status

    def get_guess_history(self):
        """Return a copy of the accepted guesses."""
        return self.guesses.copy()

    def reset_game(self, new_secret_word):
        """Start a new round with a new secret word."""
        if not isinstance(new_secret_word, str) or not new_secret_word:
            raise ValueError("Secret word must be a non-empty string")

        self.secret_word = new_secret_word.lower()
        self.guesses = []
        self.status = "ongoing"
