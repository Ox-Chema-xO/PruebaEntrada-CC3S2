from typing import List, Optional
import random
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db_models import Question, Quiz, QuizQuestion, DifficultyLevel
from datetime import datetime

class TriviaManagerDB:
    """
    Clase controladora de la lógica del juego Trivia con gestión de niveles de dificultad con db
    
    Reglas:
      - Son 10 preguntas.
      - Se inicia en nivel "fácil".
      - Si el usuario responde 3 preguntas correctas consecutivas, la dificultad sube:
            "fácil" -> "normal" y "normal" -> "difícil".
      - Si el usuario responde de manera incorrecta, no hay cambio de dificultad
    """
    def __init__(self, db: Session):
        self.db = db
        self.quiz = None
        self.total_questions = 10
        self.current_difficulty = 'fácil'  
        self.consecutive_correct = 0  
        self.current_question_index = 0
        
        self._initialize_quiz()

    def _initialize_quiz(self):
        """Inicializa un nuevo quiz en la base de datos"""
        difficulty = self.db.query(DifficultyLevel).filter(DifficultyLevel.name == self.current_difficulty).first()
        
        self.quiz = Quiz(
            current_difficulty_id=difficulty.id,
            consecutive_correct=0
        )
        self.db.add(self.quiz)
        self.db.commit()
        self.db.refresh(self.quiz)
        
        self.select_questions_by_difficulty()

    def select_questions_by_difficulty(self):
        """
        Selecciona preguntas de acuerdo al nivel de dificultad que nos encontramos.
        """
        difficulty = self.db.query(DifficultyLevel).filter(DifficultyLevel.name == self.current_difficulty).first()
        
        available_questions = self.db.query(Question).filter(
            Question.difficulty_id == difficulty.id
        ).all()
        
        random.shuffle(available_questions)
        selected_questions = available_questions[:10]

        self.db.query(QuizQuestion).filter(QuizQuestion.quiz_id == self.quiz.id).delete()
        
        for i, question in enumerate(selected_questions):
            quiz_question = QuizQuestion(
                quiz_id=self.quiz.id,
                question_id=question.id,
                question_index=i
            )
            self.db.add(quiz_question)
        
        self.current_question_index = 0
        self.db.commit()
    
    def adjust_difficulty(self):
        """
        Ajusta la dificultad en función del rendimiento del jugador.
        """
        if self.consecutive_correct >= 3:
            # Actualizar la dificultad
            if self.current_difficulty == 'fácil':
                self.current_difficulty = 'normal'
            elif self.current_difficulty == 'normal':
                self.current_difficulty = 'difícil'
            
            # Actualizar el quiz en la bd
            difficulty = self.db.query(DifficultyLevel).filter(
                DifficultyLevel.name == self.current_difficulty
            ).first()
            
            self.quiz.current_difficulty_id = difficulty.id
            self.quiz.consecutive_correct = 0
            self.consecutive_correct = 0
            
            self.db.commit()
            
            # Luego de haber ajustado la dificultados seleccionamos las nuevas preguntas
            self.select_questions_by_difficulty()

    def has_more_questions(self) -> bool:
        """
        Verificar si hay más preguntas.
        
        Returns:
            bool: True si hay más preguntas, False en caso contrario.
        """
        
        return self.current_question_index < self.total_questions

    def get_next_question(self) -> Optional[Question]:
        """
        Pasar a la siguiente pregunta.

        Returns:
            Optional[Question]: Siguiente pregunta, o None si no hay más preguntas.
        """
        if not self.has_more_questions():
            return None
        
        quiz_question = self.db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == self.quiz.id,
            QuizQuestion.question_index == self.current_question_index
        ).first()
        
        if not quiz_question:
            return None

        question = self.db.query(Question).filter(
            Question.id == quiz_question.question_id
        ).first()
        
        self.current_question_index += 1
        
        return question
        
    def answer_question(self, question: Question, answer: str) -> bool:
        """
        Procesa la respuesta del jugador a la pregunta.

        Args:
            question (Question): La pregunta a responder.
            answer (str): Respuesta del usuario.
            
        Returns:
            bool: True si la respuesta es correcta, False en caso contrario.
        """
        
        is_correct = question.is_correct(answer)
        
        quiz_question = self.db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == self.quiz.id,
            QuizQuestion.question_id == question.id
        ).first()
        
        if quiz_question:
            quiz_question.user_answer = answer
            quiz_question.is_correct = is_correct
            quiz_question.answered_at = func.now()
        
        if is_correct:
            self.quiz.correct_answers += 1
            self.consecutive_correct += 1
            self.quiz.consecutive_correct += 1
        else:
            self.quiz.incorrect_answers += 1
            self.consecutive_correct = 0
            self.quiz.consecutive_correct = 0
        
        self.db.commit()
        self.adjust_difficulty()
        
        return is_correct

    def get_score(self) -> dict:
        """
        Muestra la puntuación del jugador.
        
        Returns:
            dict: Diccionario con el total de preguntas, respuestas correctas,
                  respuestas incorrectas, la dificultad actual y la precisión.
        """
        difficulty = self.db.query(DifficultyLevel).filter(
            DifficultyLevel.id == self.quiz.current_difficulty_id
        ).first()
        
        accuracy = round((self.quiz.correct_answers / self.total_questions) * 100, 2) 
        
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.quiz.correct_answers,
            "incorrect_answers": self.quiz.incorrect_answers,
            "current_difficulty": difficulty.name,
            "accuracy": accuracy
        }
        
    def reset_game(self) -> None:
        """Restaurar el juego al estado inicial."""
        self.quiz.completed_at = datetime.now()
        self.db.commit()
        
        self.total_questions = 0
        self.current_difficulty = 'fácil'
        self.consecutive_correct = 0
        self.current_question_index = 0
        self._initialize_quiz()