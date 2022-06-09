import sqlite3
from dataclasses import dataclass
from typing import Optional, Set


@dataclass(eq=True, frozen=True)
class Contact:
    fullname: str
    address: str
    phone_number: str
    email_address: str
    id: Optional[int] = None


class Model:
    _cursor: sqlite3.Cursor

    def __init__(self, connection: sqlite3.Connection):
        self._cursor = connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self._cursor.execute(
            """
            CREATE TABLE if NOT EXISTS contact(
                id            INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
                fullname      CHAR(50)                           NOT NULL,
                address       CHAR(50)                           NOT NULL,
                phone_number  CHAR(50)                           NOT NULL,
                email_address CHAR(50)                           NOT NULL
                )
             """
        )

    def create(self, contact: Contact) -> Contact:
        self._cursor.execute(
            """
            INSERT INTO contact(fullname, address, phone_number, email_address)
            VALUES (?, ?, ?, ?)  
            """, [
                contact.fullname,
                contact.address,
                contact.phone_number,
                contact.email_address
            ]
        )

        return Contact(**{**contact.__dict__, "id": self._cursor.lastrowid})

    def get(self, *, contact_id: int) -> Contact:
        row = self._cursor.execute(
            """
            SELECT id, fullname, address, phone_number, email_address 
            FROM contact 
            WHERE id=? 
            """, [
                contact_id
            ]
        ).fetchone()

        return Contact(
            id=row[0],
            fullname=row[1],
            address=row[2],
            phone_number=row[3],
            email_address=row[4]
        )

    def list(self) -> Set[Contact]:
        rows = self._cursor.execute(
            """
            SELECT id, fullname, address, phone_number, email_address 
            FROM contact
            """).fetchall()

        return {
            Contact(
                id=row[0],
                fullname=row[1],
                address=row[2],
                phone_number=row[3],
                email_address=row[4]
            ) for row in rows
        }



