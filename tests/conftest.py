"""
Configuración global para las pruebas.
Este archivo se carga automáticamente por pytest.
"""
import pytest
import os

USE_POSTGRES_FOR_TESTS = os.environ.get("USE_POSTGRES_FOR_TESTS", "false").lower() == "true"

@pytest.fixture(scope="session")
def db_type():
    """Devuelve el tipo de base de datos que se está usando para las pruebas"""
    return "postgres" if USE_POSTGRES_FOR_TESTS else "sqlite"