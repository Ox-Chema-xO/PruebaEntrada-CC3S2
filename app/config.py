import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
SECRET_KEY = os.getenv("SECRET_KEY")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def is_development():
    return ENVIRONMENT == "development"

def is_production():
    return ENVIRONMENT == "production"

def is_testing():
    return ENVIRONMENT == "testing"

if not DATABASE_URL and not is_testing():
    raise ValueError("DATABASE_URL no está definida")

if is_testing():
    DATABASE_URL = TEST_DATABASE_URL

if is_development() and not SECRET_KEY:
    raise ValueError("SECRET_KEY debe estar definida en producción")
