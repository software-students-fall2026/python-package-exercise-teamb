'''
clean
- Make user input clean (remove spaces and chng. cases)

is_abc
- TRUE if input only uses alphabet

is_len
- TRUE if 5 letters

is_exist
- TRUE if it is an actual word

load_dict
- Load dict.txt

val_try
- Validates guess, returns (ok, message)
'''

from collections.abc import Iterable
from functools import lru_cache
from importlib import resources

WORD_LENGTH = 5           # Fixed. 5 letters only
WORDS_FILE = "dict.txt"  # Dict file. Same folder as this file


def clean(word: str) -> str:
    if not isinstance(word, str):
        raise TypeError("Word must be a str")
    return word.strip().lower()


def is_abc(word: str) -> bool:
    cleaned = clean(word)
    return cleaned.isascii() and cleaned.isalpha()


def is_len(word: str) -> bool:
    return len(clean(word)) == WORD_LENGTH


@lru_cache(maxsize=None)
def load_dict() -> frozenset[str]:
    text = resources.files(__package__).joinpath(WORDS_FILE).read_text(encoding="utf-8")
    words = set()
    for line in text.splitlines():
        line = line.strip().lower()
        if not line or line.startswith("#"):  # Skip blank lines and comments
            continue
        if len(line) == WORD_LENGTH and line.isascii() and line.isalpha():
            words.add(line)
    return frozenset(words)


def is_exist(word: str, word_list: Iterable[str] | None = None) -> bool:
    cleaned = clean(word)
    if not cleaned:
        return False
    if word_list is None:
        vocabulary = load_dict()
    else:
        if isinstance(word_list, str):
            raise TypeError("word_list should not be a single str")
        vocabulary = {clean(w) for w in word_list}
    return cleaned in vocabulary


def val_try(
    word: str,
    word_list: Iterable[str] | None = None,
    check_dictionary: bool = True,
) -> tuple[bool, str]:
    '''
    Check order: empty -> alphabet -> length -> dictionary
    - OK: (True, "")
    - Fail: (False, message for player)
    - check_dictionary=False: skip dictionary check (easy mode)
    '''
    cleaned = clean(word)
    if not cleaned:
        return False, "Please enter a word."
    if not is_abc(cleaned):
        return False, "Use alphabet only."
    if not is_len(cleaned):
        return False, f"The word must be {WORD_LENGTH} letters long."
    if check_dictionary and not is_exist(cleaned, word_list):
        return False, f"'{cleaned}' is not in the word list."
    return True, ""