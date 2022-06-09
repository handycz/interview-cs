import argparse
import sqlite3
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from src.contacts.model import Model, Contact
from src.contacts.operation import OperationResultStatus, OperationResultContact, OperationResult, \
    OperationResultContacts
from src.contacts.validation import ValidationService


def _get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="operation", help="contact book operation")

    create = subparsers.add_parser("create", help="create a contact")
    create.add_argument(
        "--name", "-n",
        required=True,
    )

    create.add_argument(
        "--address", "-a",
        required=True,
    )

    create.add_argument(
        "--phone", "-p",
        required=True,
    )

    create.add_argument(
        "--email", "-e",
        required=True,
    )

    modify = subparsers.add_parser("modify", help="modify a contact")
    modify.add_argument(
        "id",
        type=int,
    )
    modify.add_argument(
        "--name", "-n",
    )

    modify.add_argument(
        "--address", "-a",
    )

    modify.add_argument(
        "--phone", "-p",
    )

    modify.add_argument(
        "--email", "-e",
    )

    delete = subparsers.add_parser("delete", help="delete a contact")
    delete.add_argument(
        "id",
        type=int,
    )

    get = subparsers.add_parser("get", help="get a contact")
    get.add_argument(
        "id",
        type=int,
    )

    _ = subparsers.add_parser("list", help="list contacts")

    return parser.parse_args()


def _create_operation(args: argparse.Namespace) -> "Operation":
    if args.operation == "list":
        return ListOperation()
    elif args.operation == "get":
        return GetOperation(args.id)
    elif args.operation == "create":
        return CreateOperation(
            Contact(
                fullname=args.name,
                address=args.address,
                phone_number=args.phone,
                email_address=args.email,
            )
        )
    elif args.operation == "delete":
        return DeleteOperation(args.id)
    elif args.operation == "modify":
        changes = dict()

        if args.name:
            changes["fullname"] = args.name

        if args.address:
            changes["address"] = args.address

        if args.phone:
            changes["phone_number"] = args.phone

        if args.email:
            changes["email_address"] = args.email

        return ModifyOperation(args.id, changes)
    else:
        raise ValueError(f"Unknown operation {args.operation}")


def run_contact_book():
    args = _get_arguments()
    operation = _create_operation(args)
    result = operation.execute(
        ContactBook()
    )

    print(result.get_output_string())


class ContactBook:
    _model: Model
    _validation: ValidationService

    def __init__(self):
        self._validation = ValidationService()
        self._model = Model(
            sqlite3.connect("contacts.sqlite")
        )

    def create(self, contact: Contact) -> Contact:
        self._validation.is_contact_valid(contact)
        return self._model.create(contact)

    def get(self, contact_id: int) -> Optional[Contact]:
        if not isinstance(contact_id, int):
            raise ValueError("Malformed contact ID")

        return self._model.get(contact_id=contact_id)

    def list(self) -> List[Contact]:
        return self._model.list()

    def delete(self, contact_id: int):
        if not isinstance(contact_id, int):
            raise ValueError("Malformed contact ID")

        self._model.delete(contact_id=contact_id)

    def modify(self, contact_id: int, contact_changes: Dict[str, str]) -> Contact:
        original_contact = self._model.get(contact_id=contact_id)

        changed_contact = Contact(**{**original_contact.__dict__, **contact_changes})
        print(contact_changes)
        self._validation.is_contact_valid(changed_contact)

        self._model.modify(changed_contact)
        return self._model.get(contact_id=contact_id)


class Operation(ABC):
    @abstractmethod
    def execute(self, contact_book: ContactBook) -> OperationResult:
        pass


class CreateOperation(Operation):
    _contact: Contact

    def __init__(self, contact: Contact):
        self._contact = contact

    def execute(self, contact_book: ContactBook) -> OperationResult:
        try:
            created = contact_book.create(self._contact)
        except ValueError as e:
            return OperationResultStatus(False, str(e))

        return OperationResultContact(created)


class DeleteOperation(Operation):
    _contact_id: int

    def __init__(self, contact_id: int):
        self._contact_id = contact_id

    def execute(self, contact_book: ContactBook) -> OperationResult:
        try:
            contact_book.delete(self._contact_id)
        except ValueError as e:
            return OperationResultStatus(False, str(e))

        return OperationResultStatus(True)


class ModifyOperation(Operation):
    _contact_changes: Dict[str, str]
    _contact_id: int

    def __init__(self, contact_id: int, contact_changes: Dict[str, str]):
        self._contact_id = contact_id
        self._contact_changes = contact_changes

    def execute(self, contact_book: ContactBook):
        try:
            new_contact = contact_book.modify(self._contact_id, self._contact_changes)
        except ValueError as e:
            return OperationResultStatus(False, str(e))

        return OperationResultContact(new_contact)


class GetOperation(Operation):
    _contact_id: int

    def __init__(self, contact_id: int):
        self._contact_id = contact_id

    def execute(self, contact_book: ContactBook) -> OperationResult:
        try:
            contact = contact_book.get(self._contact_id)
        except ValueError as e:
            return OperationResultStatus(False, str(e))

        if contact:
            return OperationResultContact(contact)
        else:
            return OperationResultStatus(False, "Not found")


class ListOperation(Operation):
    def execute(self, contact_book: ContactBook) -> OperationResult:
        try:
            contacts = contact_book.list()
        except ValueError as e:
            return OperationResultStatus(False, str(e))

        return OperationResultContacts(contacts)
