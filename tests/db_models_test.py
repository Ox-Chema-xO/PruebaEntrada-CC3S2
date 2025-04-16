from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import json

# db de prueba para SQLite
TestBase = declarative_base()

class DifficultyLevel(TestBase):
    """Modelo para niveles de dificultad (para pruebas)"""
    __tablename__ = "difficulty_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    questions = relationship("Question", back_populates="difficulty")
    quizzes = relationship("Quiz", back_populates="current_difficulty")

class Question(TestBase):
    """Modelo para preguntas (para pruebas)"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
  
    options_json = Column(JSON, nullable=False)
    correct_answer = Column(String, nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulty_levels.id"))
    created_at = Column(TIMESTAMP)
 
    difficulty = relationship("DifficultyLevel", back_populates="questions")
    quiz_questions = relationship("QuizQuestion", back_populates="question")
    
    @property
    def options(self):
        """Getter para options"""
        return self.options_json
    
    @options.setter
    def options(self, value):
        """Setter para options"""
        self.options_json = value
    
    def is_correct(self, answer):
        """Verifica si la respuesta es correcta"""
        return self.correct_answer == answer

class Quiz(TestBase):
    """Modelo para quizzes (para pruebas)"""
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    current_difficulty_id = Column(Integer, ForeignKey("difficulty_levels.id"))
    consecutive_correct = Column(Integer, default=0)
    created_at = Column(TIMESTAMP)
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

class QuizQuestion(TestBase):
    """Modelo para la relación entre quizzes y preguntas (para pruebas)"""
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