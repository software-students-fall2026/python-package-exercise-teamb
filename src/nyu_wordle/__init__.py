'''
nyu_wordle
- Wordle-style word guessing game package

val
- Validates guesses (clean, is_abc, is_len, is_exist, load_dict, val_try)

check_guess
- Compares guess with secret word (correct / present / absent)

game
- Tracks attempts and game status (WordleGame)
'''

from .check_guess import check_guess
from .game import WordleGame
from .val import (
    WORD_LENGTH,
    clean,
    is_abc,
    is_exist,
    is_len,
    load_dict,
    val_try,
)

# Names exported by "from nyu_wordle import *"
__all__ = [
    "WORD_LENGTH",
    "WordleGame",
    "check_guess",
    "clean",
    "is_abc",
    "is_exist",
    "is_len",
    "load_dict",
    "val_try",
]