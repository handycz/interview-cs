import pytest

from src.contacts.model import Contact
from src.contacts.validation import ValidationService

VALIDATION_SERVICE = ValidationService()


def test_validation_ok():
    VALIDATION_SERVICE.is_contact_valid(
        Contact(
            fullname="Petr Petr",
            address="Ulice 123, Praha",
            phone_number="+420789789789",
            email_address="muj@gmail.com",
        )
    )


def test_validation_no_name():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="",
                address="Ulice 123, Praha",
                phone_number="+420789789789",
                email_address="muj@gmail.com",
            )
        )


def test_validation_no_address():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="Petr Petr",
                address="",
                phone_number="+420789789789",
                email_address="muj@gmail.com",
            )
        )


def test_validation_name_one_word():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="Petr",
                address="Ulice 123, Praha",
                phone_number="+420789789789",
                email_address="muj@gmail.com",
            )
        )


def test_validation_invalid_phone():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="Petr Petr",
                address="Ulice 123, Praha",
                phone_number="+420 789 789 789",
                email_address="muj@gmail.com",
            )
        )


def test_validation_invalid_phone_prefix():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="Petr Petr",
                address="Ulice 123, Praha",
                phone_number="plus420789789789",
                email_address="muj@gmail.com",
            )
        )


def test_validation_invalid_phone_prefix():
    with pytest.raises(ValueError):
        VALIDATION_SERVICE.is_contact_valid(
            Contact(
                fullname="Petr Petr",
                address="Ulice 123, Praha",
                phone_number="+420789789789",
                email_address="muj@gmailcom",
            )
        )
