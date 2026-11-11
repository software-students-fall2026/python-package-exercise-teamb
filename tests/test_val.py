import pytest

from nyu_wordle.val import (
    WORD_LENGTH,
    clean,
    is_abc,
    is_exist,
    is_len,
    load_dict,
    val_try,
)


# CLEAN

def test_clean_1():
    assert clean("CRANE") == "crane"
    assert clean("  crane  ") == "crane"
    assert clean("\tCrAnE\n") == "crane"


def test_clean_2():
    assert clean("cr ane") == "cr ane"
    assert clean("") == ""
    assert clean("   ") == ""


@pytest.mark.parametrize("bad", [None, 12345, ["crane"], b"crane"])
def test_clean_str(bad):
    with pytest.raises(TypeError):
        clean(bad)


# IS_ABC

def test_is_abc_1():
    assert is_abc("crane") is True
    assert is_abc("CRANE") is True
    assert is_abc("  crane ") is True


@pytest.mark.parametrize("word", ["cr4ne", "cr ne", "cra-e", "crané", "", "12345", "!!!!!"])
def test_is_abc_clean_1(word):
    assert is_abc(word) is False


def test_is_abc_clean_2():
    with pytest.raises(TypeError):
        is_abc(None)


# IS_LEN

def test_is_len_5():
    assert WORD_LENGTH == 5
    assert is_len("crane") is True
    assert is_len("  crane  ") is True


@pytest.mark.parametrize("word", ["", "     ", "c", "cran", "cranes", "abcdefghij"])
def test_is_len_5_else(word):
    assert is_len(word) is False


def test_is_len_clean():
    with pytest.raises(TypeError):
        is_len(12345)
    with pytest.raises(TypeError):
        is_len(None)
    with pytest.raises(TypeError):
        is_len(["c", "r", "a", "n", "e"])


# LOAD_DICT

def test_load_dict_1():
    words = load_dict()
    assert isinstance(words, frozenset)
    assert len(words) > 1000
    assert "crane" in words


def test_load_dict_contains_clean_5():
    words = load_dict()
    assert all(len(w) == WORD_LENGTH for w in words)
    assert all(w == w.lower() for w in words)
    assert all(w.isascii() and w.isalpha() for w in words)


def test_load_dict_skips_comment():
    assert not any(w.startswith("#") for w in load_dict())
    assert load_dict() is load_dict()
    assert "" not in load_dict()


# IS_EXIST

@pytest.mark.parametrize("word", ["crane", "apple", "house", "world", "CRANE", " crane "])
def test_is_exist_white(word):
    assert is_exist(word) is True


@pytest.mark.parametrize("word", ["xqzvj", "zzzzz", "aaaaa", "", "   "])
def test_is_exist_black(word):
    assert is_exist(word) is False


def test_is_exist_cust():
    custom = ["Alpha", "bravo", "CHARL"]
    assert is_exist("alpha", word_list=custom) is True
    assert is_exist("charl", word_list=custom) is True
    assert is_exist("crane", word_list=custom) is False


def test_is_exist_cust_2():
    assert is_exist("crane", word_list=[]) is False
    assert is_exist("crane", word_list=set()) is False
    assert is_exist("crane", word_list=()) is False


def test_is_exist_reject():
    with pytest.raises(TypeError):
        is_exist(None)
    with pytest.raises(TypeError):
        is_exist("crane", word_list="crane")
    with pytest.raises(TypeError):
        is_exist("crane", word_list=[1, 2, 3])


# VAL_TRY

def test_val_try_white():
    assert val_try("crane") == (True, "")
    assert val_try("  CRANE ") == (True, "")
    assert val_try("alpha", word_list=["alpha"]) == (True, "")


@pytest.mark.parametrize(
    "word, expected_message",
    [
        ("", "Please enter a word."),
        ("   ", "Please enter a word."),
        ("cr4ne", "Use alphabet only."),
        ("cr ne", "Use alphabet only."),
        ("cran", "The word must be 5 letters long."),
        ("cranes", "The word must be 5 letters long."),
        ("xqzvj", "'xqzvj' is not in the word list."),
    ],
)
def test_val_try_report(word, expected_message):
    ok, message = val_try(word)
    assert ok is False
    assert message == expected_message


def test_val_try_check_order():
# abc chk bef. len. chk
    assert val_try("c4")[1] == "Use alphabet only."
    assert val_try("abcdefg")[1] == "The word must be 5 letters long."
    assert val_try("abcde")[0] is False


def test_val_try_1():
    assert val_try("xqzvj", check_dictionary=False) == (True, "")
    assert val_try("xqzv", check_dictionary=False)[0] is False
    assert val_try("xq1vj", check_dictionary=False)[0] is False


def test_val_try_2():
    assert val_try("alpha", word_list=["alpha"]) == (True, "")
    assert val_try("planet", word_list=["planet"]) == (False, "The word must be 5 letters long.")
    assert val_try("crane", word_list=["alpha"]) == (False, "'crane' is not in the word list.")


def test_val_try_reject():
    with pytest.raises(TypeError):
        val_try(None)
    with pytest.raises(TypeError):
        val_try(12345)
    with pytest.raises(TypeError):
        val_try("crane", word_list="crane")