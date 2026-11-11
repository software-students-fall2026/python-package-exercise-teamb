from pathlib import Path

from nyu_wordle import (
    WordleGame,
    check_guess,
    clean,
    is_abc,
    is_len,
    is_exist,
    load_dict,
    val_try,
)


def display_feedback(guess, feedback):
    colors = {
        "correct": "\033[42m",
        "present": "\033[43m",
        "absent": "\033[100m",
    }
    reset = "\033[0m"

    for letter, result in zip(guess.upper(), feedback):
        print(f"{colors[result]} {letter} {reset}", end=" ")
    print()

def demonstrate_helpers():
    """Demonstrate the package's word validation functions."""
    print("\n--- NYU Wordle Helper Functions ---")

    print("clean('  TISCH  '):", clean("  TISCH  "))
    print("is_abc('tisch'):", is_abc("tisch"))
    print("is_len('tisch'):", is_len("tisch"))
    print("is_exist('tisch'):", is_exist("tisch"))

    words = load_dict()
    print("load_dict():", len(words), "valid words available")

    print("val_try('tisch'):", val_try("tisch"))
    print("---------------------------------\n")

def demonstrate_reset():
    """Demonstrate resetting a Wordle game."""
    print("\n--- Game Reset Demonstration ---")

    example_game = WordleGame("tisch")
    example_game.submit_guess("stern")

    print("Before reset:", example_game.get_guess_history())

    example_game.reset_game("stern")

    print("After reset:", example_game.get_guess_history())
    print("Game status:", example_game.get_status())
    print("--------------------------------\n")

def main():
    nyu_words_path = Path(__file__).parent / "src" / "nyu_wordle" / "nyu_words.txt"

    with open(nyu_words_path, "r") as file:
        nyu_words = [line.strip() for line in file if line.strip()]

    secret_word = WordleGame.choose_random_word(nyu_words)
    game = WordleGame(secret_word)

    demonstrate_helpers()
    demonstrate_reset()
    
    print("Welcome to NYU Wordle!")
    print("Guess the 5-letter word. You have 6 attempts.")

    while game.get_status() == "ongoing":
        guess = input("\nEnter your guess: ").strip().lower()

        valid, message = val_try(guess)

        if not valid:
            print(message)
            continue

        feedback = check_guess(guess, secret_word)
        game.submit_guess(guess)

        display_feedback(guess, feedback)
        print(f"Attempts remaining: {game.get_remaining_attempts()}")
        print(f"Guess history: {game.get_guess_history()}")

    if game.get_status() == "won":
        print("\nCongratulations! You guessed the word!")
    else:
        print(f"\nGame over! The word was {secret_word.upper()}.")


if __name__ == "__main__":
    main()
