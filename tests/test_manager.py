import pytest
import os
import sys
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db_models import Base, Question, Quiz, DifficultyLevel, QuizQuestion
from app.manager_trivia import TriviaManagerDB

# Configurar una base de datos en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Sesión de prueba
    db = TestingSessionLocal()
    
    # Añadir datos de prueba
    difficulties = [
        DifficultyLevel(name="fácil", description="Preguntas básicas"),
        DifficultyLevel(name="normal", description="Preguntas intermedias"),
        DifficultyLevel(name="difícil", description="Preguntas avanzadas")
    ]
    db.add_all(difficulties)
    db.commit()
    
    # Preguntas de prueba para cada nivel
    questions_facil = [
        Question(
            description="¿Cuál es la capital de Francia?",
            options=["Madrid", "Londres", "París", "Berlín"],
            correct_answer="París",
            difficulty_id=1
        ),
        Question(
            description="¿Cuál es el planeta más cercano al Sol?",
            options=["Venus", "Mercurio", "Tierra", "Marte"],
            correct_answer="Mercurio",
            difficulty_id=1
        )
    ]
    
    questions_normal = [
        Question(
            description="¿En qué año comenzó la Segunda Guerra Mundial?",
            options=["1939", "1940", "1941", "1945"],
            correct_answer="1939",
            difficulty_id=2
        ),
        Question(
            description="¿Cuál es el río más largo del mundo?",
            options=["Nilo", "Amazonas", "Misisipi", "Yangtsé"],
            correct_answer="Amazonas",
            difficulty_id=2
        )
    ]
    
    questions_dificil = [
        Question(
            description="¿Cuál es la partícula subatómica más pesada?",
            options=["Electrón", "Protón", "Neutrón", "Quark top"],
            correct_answer="Quark top",
            difficulty_id=3
        ),
        Question(
            description="¿Qué científico formuló la teoría cuántica?",
            options=["Einstein", "Bohr", "Planck", "Heisenberg"],
            correct_answer="Planck",
            difficulty_id=3
        )
    ]
    
    db.add_all(questions_facil + questions_normal + questions_dificil)
    db.commit()
    
    yield db
    
    # Limpieza
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_trivia_manager_init(test_db):
    """Prueba la inicialización del TriviaManager"""
    manager = TriviaManagerDB(test_db)
    
    # Verificar que se creó un quiz
    assert manager.quiz is not None
    assert manager.current_difficulty == "fácil"
    assert manager.consecutive_correct == 0
    assert manager.current_question_index == 0

def test_select_questions_by_difficulty(test_db):
    """Prueba la selección de preguntas por dificultad"""
    manager = TriviaManagerDB(test_db)
    
    # Ejecutar el método a probar
    manager.select_questions_by_difficulty()
    
    # Verificar que se seleccionaron preguntas
    quiz_questions = test_db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == manager.quiz.id
    ).all()
    
    assert len(quiz_questions) > 0
    
    # Verificar que todas las preguntas son del nivel correcto
    for qq in quiz_questions:
        question = test_db.query(Question).filter(Question.id == qq.question_id).first()
        difficulty = test_db.query(DifficultyLevel).filter(DifficultyLevel.id == question.difficulty_id).first()
        assert difficulty.name == manager.current_difficulty

def test_has_more_questions(test_db):
    """Prueba el método has_more_questions"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Verificar que hay más preguntas
    assert manager.has_more_questions() == True
    
    # Avanzar todas las preguntas
    quiz_questions_count = test_db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == manager.quiz.id
    ).count()
    
    manager.current_question_index = quiz_questions_count
    
    # Verificar que ya no hay más preguntas
    assert manager.has_more_questions() == False

def test_get_next_question(test_db):
    """Prueba el método get_next_question"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Obtener la primera pregunta
    question = manager.get_next_question()
    
    # Verificar que se obtuvo una pregunta
    assert question is not None
    assert isinstance(question, Question)
    
    # Verificar que el índice avanzó
    assert manager.current_question_index == 1

def test_answer_question_correct(test_db):
    """Prueba responder correctamente a una pregunta"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Obtener la primera pregunta
    question = manager.get_next_question()
    
    # Responder correctamente
    is_correct = manager.answer_question(question, question.correct_answer)
    
    # Verificar resultados
    assert is_correct == True
    assert manager.quiz.correct_answers == 1
    assert manager.quiz.incorrect_answers == 0
    assert manager.consecutive_correct == 1
    assert manager.quiz.consecutive_correct == 1

def test_answer_question_incorrect(test_db):
    """Prueba responder incorrectamente a una pregunta"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Obtener la primera pregunta
    question = manager.get_next_question()
    
    # Responder incorrectamente
    wrong_answer = [opt for opt in question.options if opt != question.correct_answer][0]
    is_correct = manager.answer_question(question, wrong_answer)
    
    # Verificar resultados
    assert is_correct == False
    assert manager.quiz.correct_answers == 0
    assert manager.quiz.incorrect_answers == 1
    assert manager.consecutive_correct == 0
    assert manager.quiz.consecutive_correct == 0

def test_adjust_difficulty(test_db):
    """Prueba el ajuste de dificultad después de respuestas correctas consecutivas"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Simular 3 respuestas correctas consecutivas
    manager.consecutive_correct = 3
    manager.quiz.consecutive_correct = 3
    
    # Ajustar la dificultad
    initial_difficulty = manager.current_difficulty
    manager.adjust_difficulty()
    
    # Verificar que la dificultad aumentó
    assert manager.current_difficulty != initial_difficulty
    assert manager.current_difficulty == "normal"
    assert manager.consecutive_correct == 0
    
    # Simular otras 3 respuestas correctas consecutivas
    manager.consecutive_correct = 3
    manager.quiz.consecutive_correct = 3
    
    # Ajustar la dificultad nuevamente
    manager.adjust_difficulty()
    
    # Verificar que la dificultad aumentó al máximo
    assert manager.current_difficulty == "difícil"

def test_get_score(test_db):
    """Prueba obtener la puntuación del juego"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Obtener la primera pregunta y responder correctamente
    question = manager.get_next_question()
    manager.answer_question(question, question.correct_answer)
    
    # Obtener la segunda pregunta y responder incorrectamente
    question = manager.get_next_question()
    wrong_answer = [opt for opt in question.options if opt != question.correct_answer][0]
    manager.answer_question(question, wrong_answer)
    
    # Obtener la puntuación
    score = manager.get_score()
    
    # Verificar los datos de la puntuación
    assert score["total_questions"] == 2
    assert score["correct_answers"] == 1
    assert score["incorrect_answers"] == 1
    assert score["current_difficulty"] == "fácil"
    assert score["accuracy"] == 50.0

def test_reset_game(test_db):
    """Prueba reiniciar el juego"""
    manager = TriviaManagerDB(test_db)
    
    # Asegurarse de que hay preguntas
    manager.select_questions_by_difficulty()
    
    # Obtener y responder algunas preguntas
    question = manager.get_next_question()
    manager.answer_question(question, question.correct_answer)
    
    # Guardar el ID del quiz actual
    old_quiz_id = manager.quiz.id
    
    # Reiniciar el juego
    manager.reset_game()
    
    # Verificar que se creó un nuevo quiz
    assert manager.quiz.id != old_quiz_id
    assert manager.current_difficulty == "fácil"
    assert manager.consecutive_correct == 0
    assert manager.current_question_index == 0
    assert manager.quiz.correct_answers == 0
    assert manager.quiz.incorrect_answers == 0
    
    # Verificar que el quiz anterior se marcó como completado
    old_quiz = test_db.query(Quiz).filter(Quiz.id == old_quiz_id).first()
    assert old_quiz.completed_at is not None