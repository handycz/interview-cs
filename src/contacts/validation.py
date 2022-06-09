import re

from src.contacts.model import Contact


class ValidationService:
    _email_regex: re.Pattern

    def __init__(self):
        self._email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )

    def is_contact_valid(self, contact: Contact):
        if len(contact.fullname) < 3:
            raise ValueError("Name too short")

        if " " not in contact.fullname:
            raise ValueError("Name must contain at least two words")

        if len(contact.address) < 3:
            raise ValueError("Address too short")

        self._validate_phone_number(contact)
        self._validate_mail_address(contact)

    def _validate_phone_number(self, contact: Contact):
        prefix = contact.phone_number[0]
        without_prefix = contact.phone_number[1:]

        if prefix != "+" and not prefix.isnumeric():
            raise ValueError("Phone number prefix can only be +")

        if not without_prefix.isnumeric():
            raise ValueError("Phone number must only contain numbers")

    def _validate_mail_address(self, contact: Contact):
        match = self._email_regex.match(contact.email_address)

        if not match:
            raise ValueError("Invalid e-mail address")
