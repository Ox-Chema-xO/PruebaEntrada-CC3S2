from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, ARRAY, TIMESTAMP, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import time

from app.config import DATABASE_URL

def create_db_engine(url, max_retries=5, retry_interval=5):
    """Crea el motor de base de datos con reintentos en caso de error de conexión"""
    for attempt in range(max_retries):
        try:
            print(f"Intentando conectar a la base de datos (intento {attempt+1})...")
            engine = create_engine(url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Conexión a la base de datos establecida correctamente")
            return engine
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            if attempt < max_retries - 1:
                print(f"Reintentando en {retry_interval} segundos...")
                time.sleep(retry_interval)
            else:
                print("Se agotaron los reintentos. No se pudo conectar a la base de datos.")
                raise

engine = create_db_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DifficultyLevel(Base):
    """Modelo para niveles de dificultad"""
    __tablename__ = "difficulty_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    

    questions = relationship("Question", back_populates="difficulty")
    quizzes = relationship("Quiz", back_populates="current_difficulty")

class Question(Base):
    """Modelo para preguntas"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    options = Column(ARRAY(String), nullable=False)
    correct_answer = Column(String, nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulty_levels.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
 
    difficulty = relationship("DifficultyLevel", back_populates="questions")
    quiz_questions = relationship("QuizQuestion", back_populates="question")
    
    def is_correct(self, answer):
        """Verifica si la respuesta es correcta"""
        return self.correct_answer == answer

class Quiz(Base):
    """Modelo para quizzes"""
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    current_difficulty_id = Column(Integer, ForeignKey("difficulty_levels.id"))
    consecutive_correct = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    completed_at = Column(TIMESTAMP, nullable=True)
    
    current_difficulty = relationship("DifficultyLevel", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz")
    
    def add_question(self, question, index):
        """Añade una pregunta al quiz"""
        quiz_question = QuizQuestion(
            quiz_id=self.id,
            question_id=question.id,
            question_index=index
        )
        return quiz_question
    
    def answer_question(self, question, answer):
        """Registra la respuesta a una pregunta"""
        is_correct = question.is_correct(answer)
        
        if is_correct:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1
            
        return is_correct

class QuizQuestion(Base):
    """Modelo para la relación entre quizzes y preguntas"""
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    answered_at = Column(TIMESTAMP, nullable=True)
    question_index = Column(Integer, nullable=False)
    
    quiz = relationship("Quiz", back_populates="questions")
    question = relationship("Question", back_populates="quiz_questions")

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()