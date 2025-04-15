from fastapi.testclient import TestClient
import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.db_models import Base, DifficultyLevel, Question, get_db

# Configurar una base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas en la base de datos en memoria
Base.metadata.create_all(bind=engine)

# Sobreescribir la dependencia get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Cliente de prueba
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Añadir datos de prueba
    db = TestingSessionLocal()
    
    # Agregar niveles de dificultad
    difficulties = [
        DifficultyLevel(name="fácil", description="Preguntas básicas"),
        DifficultyLevel(name="normal", description="Preguntas intermedias"),
        DifficultyLevel(name="difícil", description="Preguntas avanzadas")
    ]
    db.add_all(difficulties)
    db.commit()
    
    # Agregar preguntas de prueba
    db.add(Question(
        description="¿Cuál es la capital de Francia?",
        options=["Madrid", "Londres", "París", "Berlín"],
        correct_answer="París",
        difficulty_id=1
    ))
    db.commit()
    
    yield db
    
    # Limpieza
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_read_root(test_db):
    """Prueba el endpoint de bienvenida"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "¡Bienvenido a la API de Trivia!"

def test_start_game(test_db):
    """Prueba iniciar un nuevo juego"""
    response = client.get("/start-game")
    assert response.status_code == 200
    assert "quiz_id" in response.json()
    assert isinstance(response.json()["quiz_id"], int)

def test_get_next_question(test_db):
    """Prueba obtener la siguiente pregunta"""
    # Primero iniciamos un juego
    start_response = client.get("/start-game")
    quiz_id = start_response.json()["quiz_id"]
    
    # Luego obtenemos la primera pregunta
    response = client.get(f"/game/{quiz_id}/next-question")
    assert response.status_code == 200
    
    # Verificamos que contiene los datos esperados
    data = response.json()
    assert "question_number" in data
    assert "description" in data
    assert "options" in data
    assert "difficulty" in data
    
    # Verificamos que las opciones son una lista
    assert isinstance(data["options"], list)
    assert len(data["options"]) > 0

def test_answer_question(test_db):
    """Prueba responder una pregunta"""
    # Primero iniciamos un juego
    start_response = client.get("/start-game")
    quiz_id = start_response.json()["quiz_id"]
    
    # Luego obtenemos la primera pregunta
    question_response = client.get(f"/game/{quiz_id}/next-question")
    
    # Obtenemos la pregunta de la base de datos
    db = next(override_get_db())
    question = db.query(Question).first()
    
    # Enviamos una respuesta correcta
    answer_data = {
        "question_id": question.id,
        "answer": question.correct_answer
    }
    
    response = client.post(f"/game/{quiz_id}/answer", json=answer_data)
    assert response.status_code == 200
    
    # Verificamos la respuesta
    data = response.json()
    assert "is_correct" in data
    assert data["is_correct"] == True
    assert "correct_answer" in data
    assert data["correct_answer"] == question.correct_answer

def test_get_score(test_db):
    """Prueba obtener la puntuación"""
    # Primero iniciamos un juego
    start_response = client.get("/start-game")
    quiz_id = start_response.json()["quiz_id"]
    
    # Obtenemos la puntuación
    response = client.get(f"/game/{quiz_id}/score")
    assert response.status_code == 200
    
    # Verificamos los datos de la puntuación
    data = response.json()
    assert "total_questions" in data
    assert "correct_answers" in data
    assert "incorrect_answers" in data
    assert "current_difficulty" in data
    assert "accuracy" in data