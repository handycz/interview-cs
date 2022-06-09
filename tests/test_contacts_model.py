import sqlite3

from src.contacts.model import Model, Contact

CONTACTS = {
    Contact(
        fullname="Jan Opicka",
        address="Zlin",
        phone_number="+420777888999",
        email_address="muj@mail.cz"
    ),
    Contact(
        fullname="Petr Mroz",
        address="Plzen",
        phone_number="+420999888777",
        email_address="jeho@e-mail.cz"
    ),
    Contact(
        fullname="Jiri Kun",
        address="CB",
        phone_number="+420888777999",
        email_address="cizi@schranka.com"
    )
}


def test_create_model(database: sqlite3.Connection):
    _ = Model(database)

    cursor = database.cursor()
    tables = {
        value[0]
        for value in cursor.execute("SELECT name FROM `sqlite_master`").fetchall()
    }
    table_column_names = {
        value[1]
        for value in cursor.execute("PRAGMA table_info(contact)").fetchall()
    }

    assert tables == {"contact", "sqlite_sequence"}
    assert table_column_names == {"id", "fullname", "address", "phone_number", "email_address"}


def test_create_contacts(database: sqlite3.Connection):
    model = Model(database)
    expected_contacts = set()

    for contact in CONTACTS:
        expected_contacts.add(
            model.create(contact)
        )

    cursor = database.cursor()

    fetched_raw_contacts = cursor.execute(
        "SELECT id, fullname, address, phone_number, email_address FROM contact"
    ).fetchall()

    fetched_contacts = {
        Contact(
            id=raw_contact[0],
            fullname=raw_contact[1],
            address=raw_contact[2],
            phone_number=raw_contact[3],
            email_address=raw_contact[4],
        ) for raw_contact in fetched_raw_contacts
    }

    assert expected_contacts == fetched_contacts


def test_get_contact(database: sqlite3.Connection):
    model = Model(database)

    input_contact = CONTACTS.copy().pop()
    expected_contact = model.create(input_contact)
    fetched_contact = model.get(contact_id=expected_contact.id)

    assert fetched_contact == expected_contact


def test_get_nonexistent_contact(database: sqlite3.Connection):
    model = Model(database)

    fetched_contact = model.get(contact_id=1234)

    assert fetched_contact is None


def test_list_contacts(database: sqlite3.Connection):
    model = Model(database)
    expected_contacts = set()

    for contact in CONTACTS:
        expected_contacts.add(
            model.create(contact)
        )

    fetched_contacts = set(model.list())

    assert fetched_contacts == expected_contacts


def test_delete_contact(database: sqlite3.Connection):
    model = Model(database)
    expected_contacts = set()

    for contact in CONTACTS:
        expected_contacts.add(
            model.create(contact)
        )

    deleted_contact = expected_contacts.pop()
    model.delete(contact_id=deleted_contact.id)
    remaining_contacts = set(model.list())

    assert remaining_contacts == expected_contacts


def test_modify_contact(database: sqlite3.Connection):
    model = Model(database)
    expected_contacts = set()

    for contact in CONTACTS:
        expected_contacts.add(
            model.create(contact)
        )

    modified_contact = Contact(**{
        **expected_contacts.pop().__dict__,
        "fullname": "Modified User",
        "phone_number": "+123321123231"
    })
    expected_contacts.add(modified_contact)

    model.modify(modified_contact)
    fetched_contacts = set(model.list())

    assert fetched_contacts == expected_contacts
