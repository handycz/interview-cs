import sqlite3

from src.contacts.model import Model


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

