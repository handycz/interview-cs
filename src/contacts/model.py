import sqlite3
from dataclasses import dataclass
from typing import Optional, Set, List


@dataclass(eq=True, frozen=True)
class Contact:
    fullname: str
    address: str
    phone_number: str
    email_address: str
    id: Optional[int] = None


class Model:
    _connection: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
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
        self._connection.commit()

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
        self._connection.commit()

        return Contact(**{**contact.__dict__, "id": self._cursor.lastrowid})

    def get(self, *, contact_id: int) -> Optional[Contact]:
        row = self._cursor.execute(
            """
            SELECT id, fullname, address, phone_number, email_address 
            FROM contact 
            WHERE id=? 
            """, [
                contact_id
            ]
        ).fetchone()

        if not row:
            return None

        return Contact(
            id=row[0],
            fullname=row[1],
            address=row[2],
            phone_number=row[3],
            email_address=row[4]
        )

    def list(self) -> List[Contact]:
        rows = self._cursor.execute(
            """
            SELECT id, fullname, address, phone_number, email_address 
            FROM contact
            ORDER BY id
            """).fetchall()

        return [
            Contact(
                id=row[0],
                fullname=row[1],
                address=row[2],
                phone_number=row[3],
                email_address=row[4]
            ) for row in rows
        ]

    def delete(self, *, contact_id: int):
        self._cursor.execute(
            """
            DELETE FROM contact
            WHERE id=?
            """, [
                contact_id
            ]
        )
        self._connection.commit()

    def modify(self, contact: Contact):
        self._cursor.execute(
            """
            UPDATE contact
            SET fullname=?,
                phone_number=?,
                address=?,
                email_address=?
            WHERE id=?
            """, [
                contact.fullname,
                contact.phone_number,
                contact.address,
                contact.email_address,
                contact.id,
            ]
        )
        self._connection.commit()
