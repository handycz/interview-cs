import sqlite3
from dataclasses import dataclass


@dataclass
class Contact:
    name: str
    address: str
    phone_number: str
    email_address: str


class Model:
    _cursor: sqlite3.Cursor

    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self._cursor.execute(
            """
            CREATE TABLE if NOT EXISTS contact(
                id            INT PRIMARY KEY AUTOINCREMENT  NOT NULL,
                fullname      CHAR(50)                       NOT NULL,
                address       CHAR(50)                       NOT NULL,
                phone_number  CHAR(50)                       NOT NULL,
                email_address CHAR(50)                       NOT NULL
                )
             """
        )

    # def create(self, contact: Contact):
    #     self._cursor.execute(
    #         """
    #         INSERT INTO
    #         """
    #     )

