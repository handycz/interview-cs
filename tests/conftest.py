import sqlite3

import pytest


@pytest.fixture(scope="function")
def database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    yield connection
    connection.close()
