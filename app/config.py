import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:trivia@db:5432/trivia_db")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
SECRET_KEY = os.getenv("SECRET_KEY", "default_insecure_key")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:trivia@db:5432/trivia_test_db")

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "trivia")
POSTGRES_DB = os.getenv("POSTGRES_DB", "trivia_db")

if ENVIRONMENT == "production" and SECRET_KEY == "default_insecure_key":
    raise ValueError("SECRET_KEY debe ser definido en producción")

def is_development():
    """Verifica si estamos en entorno de desarrollo"""
    return ENVIRONMENT == "development"

def is_production():
    """Verifica si estamos en entorno de producción"""
    return ENVIRONMENT == "production"

def is_testing():
    """Verifica si estamos en entorno de pruebas"""
    return ENVIRONMENT == "testing"

if is_testing():
    # Usar la base de datos de prueba en el entorno de testing
    DATABASE_URL = TEST_DATABASE_URL