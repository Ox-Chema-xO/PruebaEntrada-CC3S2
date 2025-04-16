import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Añadir el directorio raíz al path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos los modelos adaptados para SQLite
from tests.db_models_test import TestBase, Question, Quiz, DifficultyLevel, QuizQuestion

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    TestBase.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    yield db
    
    db.close()
    TestBase.metadata.drop_all(bind=engine)

def test_create_difficulty(test_db):
    """Prueba crear un nivel de dificultad"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()
    
    saved = test_db.query(DifficultyLevel).filter(DifficultyLevel.name == "test").first()
    assert saved is not None
    assert saved.name == "test"
    assert saved.description == "test description"

def test_create_question(test_db):
    """Prueba crear una pregunta"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()
    
    question = Question(
        description="Test question?",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        correct_answer="Option 3",
        difficulty_id=difficulty.id
    )
    test_db.add(question)
    test_db.commit()
    
    saved = test_db.query(Question).filter(Question.description == "Test question?").first()
    assert saved is not None
    assert saved.description == "Test question?"
    assert len(saved.options) == 4
    assert saved.correct_answer == "Option 3"
    assert saved.difficulty_id == difficulty.id

def test_question_is_correct(test_db):
    """Prueba el método is_correct de la clase Question"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()
    
    question = Question(
        description="Test question?",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        correct_answer="Option 3",
        difficulty_id=difficulty.id
    )
    test_db.add(question)
    test_db.commit()
    
    assert question.is_correct("Option 3") == True
    assert question.is_correct("Option 1") == False
    assert question.is_correct("Wrong answer") == False

def test_create_quiz(test_db):
    """Prueba crear un quiz"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()
    
    quiz = Quiz(
        current_difficulty_id=difficulty.id,
        consecutive_correct=0
    )
    test_db.add(quiz)
    test_db.commit()
    
    saved = test_db.query(Quiz).first()
    assert saved is not None
    assert saved.current_difficulty_id == difficulty.id
    assert saved.consecutive_correct == 0
    assert saved.correct_answers == 0
    assert saved.incorrect_answers == 0

def test_quiz_answer_question(test_db):
    """Prueba el método answer_question de la clase Quiz"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()

    question = Question(
        description="Test question?",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        correct_answer="Option 3",
        difficulty_id=difficulty.id
    )
    test_db.add(question)
    test_db.commit()

    quiz = Quiz(
        current_difficulty_id=difficulty.id,
        consecutive_correct=0
    )
    test_db.add(quiz)
    test_db.commit()
    
    is_correct = quiz.answer_question(question, "Option 3")
    test_db.commit()
    
    assert is_correct == True
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 0
    
    is_correct = quiz.answer_question(question, "Option 1")
    test_db.commit()
    
    assert is_correct == False
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 1

def test_quiz_add_question(test_db):
    """Prueba el método add_question de la clase Quiz"""
    difficulty = DifficultyLevel(name="test", description="test description")
    test_db.add(difficulty)
    test_db.commit()
    
    question = Question(
        description="Test question?",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        correct_answer="Option 3",
        difficulty_id=difficulty.id
    )
    test_db.add(question)
    test_db.commit()
    
    quiz = Quiz(
        current_difficulty_id=difficulty.id,
        consecutive_correct=0
    )
    test_db.add(quiz)
    test_db.commit()
    
    quiz_question = quiz.add_question(question, 0)
    test_db.add(quiz_question)
    test_db.commit()
    
    saved = test_db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == quiz.id,
        QuizQuestion.question_id == question.id
    ).first()
    
    assert saved is not None
    assert saved.quiz_id == quiz.id
    assert saved.question_id == question.id
    assert saved.question_index == 0