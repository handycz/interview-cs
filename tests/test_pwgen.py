import string
import sys
from unittest.mock import patch

import pytest

from src.pwgen import generate_password, has_all_characters, parse_input, run_pwgen

FULL_CHAR_WORDLIST = [
    "Ahoj",
    "Svete",
    "Snad",
    "Tady",
    "Budou",
    "Vsechna",
    "Pismena",
    "Fakt",
    "Genialni",
    "Quido",
    "World",
    "Xenie",
    "Zebra",
    "Raketa",
]


def test_has_all_characters():
    assert has_all_characters(string.ascii_letters)


def test_has_not_all_characters():
    assert not has_all_characters("abcdef")


def test_gen_password_ok():
    password = generate_password(FULL_CHAR_WORDLIST)

    assert has_all_characters(password)
    assert len(password) >= 8


def test_gen_password_short():
    with pytest.raises(ValueError):
        generate_password(["A", "B"])


def test_gen_password_no_diverse_characters():
    with pytest.raises(ValueError):
        generate_password(["Abcd", "Efgh"])


def test_parse_input():
    wordlist = parse_input(FULL_CHAR_WORDLIST)
    assert wordlist == FULL_CHAR_WORDLIST


def test_parse_input_stripped():
    wordlist = parse_input([
        "Few",
        " words",
        "with",
        "trailing   ",
        """
        spaces
        """,
    ])

    assert wordlist == [
        "Few",
        "words",
        "with",
        "trailing",
        "spaces",
    ]


def test_parse_input_spaces():
    with pytest.raises(ValueError):
        parse_input([
            "Few",
            " words",
            "with",
            "spaces in between",
        ])


def test_app():
    testargs = ["prog"] + FULL_CHAR_WORDLIST
    with patch.object(sys, "argv", testargs):
        password = run_pwgen()

    contains_wordlist_word = [
        word in password for word in FULL_CHAR_WORDLIST
    ]

    assert all(contains_wordlist_word)
    assert has_all_characters(password)
    assert len(password) >= 8
