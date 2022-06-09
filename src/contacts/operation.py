from abc import ABC, abstractmethod
from typing import List, Optional

from src.contacts.model import Contact


class OperationResult(ABC):
    @abstractmethod
    def get_output_string(self) -> str:
        pass


class OperationResultStatus(OperationResult):
    _ok: bool
    _message: Optional[str]

    def __init__(self, ok: bool, message: Optional[str] = None):
        self._ok = ok
        self._message = message

    def get_output_string(self) -> str:
        if self._ok:
            return "> OK"
        else:
            return f"> FAILED: {self._message or ''}"


class OperationResultContacts(OperationResult):
    _contacts: List[Contact]

    def __init__(self, contacts: List[Contact]):
        self._contacts = contacts

    def get_output_string(self) -> str:
        table_format = "{:<5} {:<30} {:<30} {:<15} {:<40}\n"
        out = [table_format.format("ID", "Name", "E-mail", "Phone", "Address")]

        for contact in self._contacts:
            out += [
                table_format.format(
                    contact.id,
                    contact.fullname,
                    contact.email_address,
                    contact.phone_number,
                    contact.address
                )
            ]

        return "".join(out)


class OperationResultContact(OperationResultContacts):
    def __init__(self, contact: Contact):
        super().__init__([contact])


