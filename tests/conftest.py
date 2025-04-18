import pytest
import os

USE_POSTGRES_FOR_TESTS = os.environ.get("USE_POSTGRES_FOR_TESTS", "false").lower() == "true"

@pytest.fixture(scope="session")
def db_type():
    return "postgres" if USE_POSTGRES_FOR_TESTS else "sqlite"