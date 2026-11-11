# Python Package Exercise - Team B

[![log github events](https://github.com/software-students-fall2026/python-package-exercise-teamb/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-teamb/actions/workflows/event-logger.yml)

# Subject - NYU Wordle package

Teammates:
- [Yihyun Nam](https://github.com/iindes/)
- [Sally Hegab](https://github.com/sallyhegab/)
- [Saajid Rohman](https://github.com/sar9249)
- [Scott Kim](https://github.com/jk8308-jpg)

## Description
<span style="float: left; font-size: 3em; line-height: 1; font-weight: bold; margin-right: 8px; color: #333;">N</span> YU Wordle is a fun Python package for building a wordle-style game with N. Y. U. exclusive words!
A secret 5 letter word is chosen, and the player has 6 guesses.
Each guess has an outcome of either:
- CORRECT
- PRESENT
- ABSENT

The package is split into three modules:
 
| Module | Purpose | Main items |
|---|---|---|
| `nyu_wordle.val` | Checks that a guess is a real, five-letter, letters-only word | `clean`, `is_abc`, `is_len`, `is_exist`, `load_dict`, `val_try` |
| `nyu_wordle.check_guess` | Compares a guess with the secret word, letter by letter | `check_guess` |
| `nyu_wordle.game` | Keeps track of attempts, wins, losses, and new rounds | `WordleGame` |

Here is a typical flow:
```
player input -> val_try (is it a valid word?) -> check_guess (letter results) -> WordleGame.submit_guess (update attempts and status)
```

## Package Page Link
The package is published on PyPI:
[INSERT LNK]

## Import Instruction
### Install
 
Python 3.11 or newer is required.
 
```bash
pip install [INSERT PKG NAME]
```
 
The import name is `nyu_wordle`.
 
### Quick start: a complete game in your terminal
 
Save the following as `play.py` and run `python play.py`.
 
```python
from nyu_wordle.val import val_try, clean
from nyu_wordle.check_guess import check_guess
from nyu_wordle.game import WordleGame
 
secret = WordleGame.choose_random_word(["crane", "bobst", "tisch"])
game = WordleGame(secret, max_attempts=6)
 
while game.get_status() == "ongoing":
    guess = input(f"Guess ({game.get_remaining_attempts()} left): ")
    ok, message = val_try(guess)
    if not ok:
        print(message)  # an invalid guess does not use up attempt
        continue
    guess = clean(guess)
    print(check_guess(guess, game.secret_word))
    game.submit_guess(guess)
 
print(f"You {game.get_status()}! The word was {game.secret_word.upper()}.")
```
 
### Example program
 
A full example that uses every function in the package is in [`examples/demo.py`](./examples/demo.py).

## Set up the virtual environment, install dependencies, and build and test

### 1. Prerequisites
 
- [Python](https://www.python.org/downloads/) 3.11 or newer
- [Git](https://git-scm.com/downloads)
- [pipenv](https://pipenv.pypa.io/en/latest/installation.html). The recommended way to install it is with [pipx](https://pipx.pypa.io/stable/installation/):
| OperSys | Cmd. |
|---|---|
| macOS | `brew install pipx` -> `pipx ensurepath` -> `pipx install pipenv` |
| Windows | `py -m pip install --user pipx` -> `py -m pipx ensurepath` -> `pipx install pipenv` |
 
Open a new terminal after `pipx ensurepath`
Check with `pipenv --version`.
 
### 2. Clone the repository
 
```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-teamb.git
cd python-package-exercise-teamb
```
 
### 3. Create the virtual environment and install dependencies
 
```bash
pipenv install --dev
```
 
### 4. Run the tests
 
```bash
pipenv run pytest -v
```
 
### 5. Build the package
 
```bash
pipenv run python -m build
```
 
### 6. Publish a new version (maintainers only)
 
1. Raise the `version` in `pyproject.toml`. PyPI does not accept the same version number twice.
2. Delete the old `dist/` folder and build again (step 5).
3. Upload with [twine](https://twine.readthedocs.io/). When asked for a username, enter `__token__`; the password is your PyPI API token.
```bash
pipenv run twine upload --repository testpypi dist/*   # optional dry run on TestPyPI
pipenv run twine upload dist/*
```
 
### Contribution workflow
 
- Never commit directly to `main`. Create a feature branch for every change.
- Open a pull request into **this team repository's** `main` branch (not the instructor's original repository).
- A teammate reviews the code and runs `pipenv run pytest` before approving.
- GitHub Actions builds the package and runs the tests on two Python versions for every pull request. Merge only after the checks pass.

## Configure and Run
 
### Run the example program from a clone of this repository
 
```bash
pipenv run python examples/demo.py
```
 
### Run the game after installing from PyPI
 
Install the package (GOTO [Import Instruction](#import-instruction)), save the quick start code as `play.py`, and run:
 
```bash
python play.py
```
 
On Windows, use `py play.py` if `python` is not recognized.
 
### Options you can change
 
| Option | Where | Default | Effect |
|---|---|---|---|
| `max_attempts` | `WordleGame(...)` | `6` | Number of guesses per round |
| `word_list` | `val_try(...)`, `is_exist(...)` | built-in dictionary | Accept only words from your own list |
| `check_dictionary` | `val_try(...)` | `True` | `False` accepts any five letters (easy mode) |
| Secret word pool | `WordleGame.choose_random_word(...)` | none | The list the secret word is picked from |
 
## Setting up Env. Var / Importer
 
**No setup is required!!!!**
This package does not use:
- Env. Var.,
- API keys,
- dot env,
and/or
- D\B.
 
`src/nyu_wordle/dict.txt` is bundled inside the package and installed automatically with `pip`.
 
To add words to the dictionary (for dev.):
 
1. Open `src/nyu_wordle/dict.txt`.
2. Add one lowercase five-letter word per line. Lines starting with `#` are ignored.
3. Run `pipenv run pytest` to make sure everything passes.

## Word List Credits
 
See comment in `src/nyu_wordle/dict.txt`
 
## License
 
See [LICENSE](./LICENSE)


