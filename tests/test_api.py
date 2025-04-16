from fastapi.testclient import TestClient
import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

from app.db_models import Question, DifficultyLevel, Quiz, QuizQuestion

client = TestClient(app)

#En especial para test_get_score
mock_total_questions = 0
mock_correct_answers = 0
mock_incorrect_answers = 0

@pytest.fixture
def mock_db():
    """Crea un mock de la sesión de base de datos"""
    mock_session = MagicMock()
    
    mock_difficulty = MagicMock(spec=DifficultyLevel)
    mock_difficulty.id = 1
    mock_difficulty.name = "fácil"
    
    mock_session.query.return_value.filter.return_value.first.return_value = mock_difficulty
    
    mock_quiz = MagicMock(spec=Quiz)
    mock_quiz.id = 1
    mock_quiz.current_difficulty_id = 1
    mock_quiz.correct_answers = 0
    mock_quiz.incorrect_answers = 0
    mock_quiz.consecutive_correct = 0
    mock_session.add.return_value = None
    
    def refresh_mock(obj):
        obj.id = 1
    
    mock_session.refresh.side_effect = refresh_mock
    
    return mock_session

class MockTriviaManager:
    def __init__(self, db):
        self.db = db
        self.quiz = MagicMock(spec=Quiz)
        self.quiz.id = 1
        self.quiz.current_difficulty_id = 1

        global mock_correct_answers, mock_incorrect_answers
        self.quiz.correct_answers = mock_correct_answers
        self.quiz.incorrect_answers = mock_incorrect_answers
        self.current_difficulty = "fácil"
        self.consecutive_correct = 0
        self.current_question_index = 0
        self.total_questions = mock_correct_answers + mock_incorrect_answers
    
    def has_more_questions(self):
        return True
    
    def get_next_question(self):
        question = MagicMock(spec=Question)
        question.id = 1
        question.description = "¿Cuál es la capital de Francia?"
        question.options = ["Madrid", "Londres", "París", "Berlín"]
        question.correct_answer = "París"
        question.difficulty = MagicMock(spec=DifficultyLevel)
        question.difficulty.name = "fácil"
        return question
    
    def answer_question(self, question, answer):
        global mock_total_questions, mock_correct_answers, mock_incorrect_answers
        is_correct = answer == "París"
        if is_correct:
            mock_correct_answers += 1
            self.quiz.correct_answers = mock_correct_answers
            self.consecutive_correct += 1
        else:
            mock_incorrect_answers += 1
            self.quiz.incorrect_answers = mock_incorrect_answers
            self.consecutive_correct = 0
        mock_total_questions += 1
        self.total_questions = mock_total_questions
        return is_correct
    
    def get_score(self):
        global mock_total_questions, mock_correct_answers, mock_incorrect_answers
        total = mock_correct_answers + mock_incorrect_answers
        accuracy = round((mock_correct_answers / total * 100) if total > 0 else 0, 2)
        return {
            "total_questions": total,
            "correct_answers": mock_correct_answers,
            "incorrect_answers": mock_incorrect_answers,
            "current_difficulty": self.current_difficulty,
            "accuracy": accuracy
        }

def mock_load_game_not_found(quiz_id, db):
    if quiz_id == 999:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return MockTriviaManager(db)

@pytest.fixture(autouse=True)
def patch_dependencies(mock_db):
    """Parchea las dependencias para usar mocks en las pruebas"""
 
    with patch("app.main.get_db", return_value=mock_db), \
         patch("app.main.TriviaManagerDB", MockTriviaManager), \
         patch("app.main.load_game", side_effect=lambda quiz_id, db: MockTriviaManager(db)):
        yield

@pytest.fixture(autouse=True)
def reset_mock_state():
    """Reinicia el estado global de los mocks antes de cada prueba"""
    global mock_total_questions, mock_correct_answers, mock_incorrect_answers
    mock_total_questions = 0
    mock_correct_answers = 0
    mock_incorrect_answers = 0
    yield

def test_read_root():
    """Prueba el endpoint de bienvenida"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Bienvenido a la API de Trivia!"}

def test_start_game():
    """Prueba iniciar un nuevo juego"""
    response = client.get("/start-game")
    assert response.status_code == 200
    assert "quiz_id" in response.json()
    assert response.json()["quiz_id"] == 1

def test_get_next_question():
    """Prueba obtener la siguiente pregunta"""
    response = client.get("/game/1/next-question")
    assert response.status_code == 200
    
    data = response.json()
    assert "question_number" in data
    assert "description" in data
    assert "options" in data
    assert "difficulty" in data
    
    assert data["description"] == "¿Cuál es la capital de Francia?"
    assert "París" in data["options"]
    assert data["difficulty"] == "fácil"

def test_answer_question_correct():
    """Prueba responder correctamente a una pregunta"""
    answer_data = {
        "question_id": 1,
        "answer": "París"
    }
    
    response = client.post("/game/1/answer", json=answer_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_correct"] == True
    assert data["correct_answer"] == "París"

def test_answer_question_incorrect():
    """Prueba responder incorrectamente a una pregunta"""
    answer_data = {
        "question_id": 1,
        "answer": "Madrid"
    }
    
    response = client.post("/game/1/answer", json=answer_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["is_correct"] == False
    assert data["correct_answer"] == "París"

def test_get_score():
    """Prueba obtener la puntuación"""
    client.post("/game/1/answer", json={"question_id": 1, "answer": "París"})
    client.post("/game/1/answer", json={"question_id": 1, "answer": "Madrid"})
    
    response = client.get("/game/1/score")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_questions"] == 2
    assert data["correct_answers"] == 1
    assert data["incorrect_answers"] == 1
    assert data["current_difficulty"] == "fácil"
    assert data["accuracy"] == 50.0

def test_get_next_question_no_more_questions():
    """Prueba intentar obtener una pregunta cuando no hay más disponibles"""
    with patch.object(MockTriviaManager, "has_more_questions", return_value=False):
        response = client.get("/game/1/next-question")
        assert response.status_code == 200
        assert response.json() == {"message": "No hay más preguntas disponibles"}

def test_game_not_found():
    """Prueba intentar acceder a un juego que no existe"""
    with patch("app.main.load_game", side_effect=mock_load_game_not_found):
        response = client.get("/game/999/next-question")
        assert response.status_code == 404
        assert "detail" in response.json()
        assert "no encontrado" in response.json()["detail"].lower()