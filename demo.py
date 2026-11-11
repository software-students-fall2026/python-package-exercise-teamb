import random

from nyu_wordle import WordleGame, check_guess, load_dict, val_try


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


def main():
    words = sorted(load_dict())
    secret_word = random.choice(words)
    game = WordleGame(secret_word)

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

    if game.get_status() == "won":
        print("\nCongratulations! You guessed the word!")
    else:
        print(f"\nGame over! The word was {secret_word.upper()}.")


if __name__ == "__main__":
    main()
