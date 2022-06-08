import sqlite3

from src.contacts.model import Model, Contact


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
    input_contacts = {
        Contact(
            fullname="Jan Opicka",
            address="Zlin",
            phone_number="+420 777 888 999",
            email_address="muj@mail.cz"
        ),
        Contact(
            fullname="Petr Mroz",
            address="Plzen",
            phone_number="+420 999 888 777",
            email_address="jeho@e-mail.cz"
        )
    }

    for contact in input_contacts:
        model.create(contact)

    cursor = database.cursor()

    fetched_raw_contacts = cursor.execute(
        "SELECT fullname, address, phone_number, email_address FROM contact"
    ).fetchall()

    fetched_contacts = {
        Contact(
            fullname=raw_contact[0],
            address=raw_contact[1],
            phone_number=raw_contact[2],
            email_address=raw_contact[3]
        ) for raw_contact in fetched_raw_contacts
    }

    assert input_contacts == fetched_contacts