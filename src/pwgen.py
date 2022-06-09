import string
import random
import sys
from typing import List

PW_MIN_LENGTH = 8


def run_pwgen() -> str:
    words = parse_input(
        sys.argv[1:]
    )

    password = generate_password(words)

    return password


def parse_input(input_strings: List[str]) -> List[str]:
    stripped_strings = [
        input_string.strip() for input_string in input_strings
    ]

    for stripped_string in stripped_strings:
        if " " in stripped_string:
            raise ValueError("A word cannot contain a space")

    return stripped_strings


def generate_password(words: List[str]) -> str:
    password = ""
    random.shuffle(words)

    for word in words:
        password += word

        if len(password) >= PW_MIN_LENGTH and has_all_characters(password):
            return password

    if len(password) < PW_MIN_LENGTH:
        raise ValueError("Wordlist insufficiently long")

    raise ValueError("Not enough diverse characters in the wordlist")


def has_all_characters(word: str) -> bool:
    word_lower = word.lower()

    for char in string.ascii_lowercase:
        if char not in word_lower:
            return False

    return True
