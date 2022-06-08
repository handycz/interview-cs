import sqlite3

import pytest


@pytest.fixture(scope="function")
def database() -> sqlite3.Connection:
    connection = sqlite3.connect("file::memory:?cache=shared")
    yield connection
    connection.close()
