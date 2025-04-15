from typing import List, Optional
import random
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db_models import Question, Quiz, QuizQuestion, DifficultyLevel

class TriviaManagerDB:
    """
    Clase controladora de la lógica del juego Trivia con gestión de niveles de dificultad.
    Versión adaptada para trabajar con base de datos PostgreSQL.
    
    Reglas:
      - El juego siempre es de 10 preguntas.
      - Se inicia en nivel "fácil".
      - Si el usuario responde 3 preguntas correctas consecutivas, la dificultad sube:
            "fácil" -> "normal" y "normal" -> "difícil".
      - Las respuestas incorrectas no modifican la dificultad.
    """
    def __init__(self, db: Session):
        self.db = db
        self.quiz = None
        self.total_questions = 0
        self.current_difficulty = 'fácil'  # Nivel inicial
        self.consecutive_correct = 0  # Contador de respuestas correctas consecutivas
        self.current_question_index = 0
        
        # Inicializar un nuevo quiz
        self._initialize_quiz()

    def _initialize_quiz(self):
        """Inicializa un nuevo quiz en la base de datos"""
        # Obtener el ID del nivel de dificultad 'fácil'
        difficulty = self.db.query(DifficultyLevel).filter(DifficultyLevel.name == self.current_difficulty).first()
        
        # Crear un nuevo quiz
        self.quiz = Quiz(
            current_difficulty_id=difficulty.id,
            consecutive_correct=0
        )
        self.db.add(self.quiz)
        self.db.commit()
        self.db.refresh(self.quiz)
        
        # Seleccionar preguntas según la dificultad actual
        self.select_questions_by_difficulty()

    def load_questions(self):
        """
        Esta función se mantiene por compatibilidad, pero ya no es necesaria
        ya que las preguntas se cargan desde la base de datos en el script seed.sql
        """
        pass

    def select_questions_by_difficulty(self):
        """
        Selecciona preguntas para el quiz basadas exclusivamente en la dificultad actual.
        """
        # Obtener el nivel de dificultad actual
        difficulty = self.db.query(DifficultyLevel).filter(DifficultyLevel.name == self.current_difficulty).first()
        
        # Obtener todas las preguntas de la dificultad actual
        available_questions = self.db.query(Question).filter(
            Question.difficulty_id == difficulty.id
        ).all()
        
        # Seleccionar 10 preguntas aleatorias (o menos si no hay suficientes)
        random.shuffle(available_questions)
        selected_questions = available_questions[:10]
        
        # Eliminar las preguntas anteriores del quiz actual
        self.db.query(QuizQuestion).filter(QuizQuestion.quiz_id == self.quiz.id).delete()
        
        # Añadir las nuevas preguntas al quiz
        for i, question in enumerate(selected_questions):
            quiz_question = QuizQuestion(
                quiz_id=self.quiz.id,
                question_id=question.id,
                question_index=i
            )
            self.db.add(quiz_question)
        
        # Actualizar el índice de pregunta actual
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
            
            # Actualizar el quiz en la base de datos
            difficulty = self.db.query(DifficultyLevel).filter(
                DifficultyLevel.name == self.current_difficulty
            ).first()
            
            self.quiz.current_difficulty_id = difficulty.id
            self.quiz.consecutive_correct = 0
            self.consecutive_correct = 0
            
            self.db.commit()
            
            # Seleccionar nuevas preguntas según la nueva dificultad
            self.select_questions_by_difficulty()

    def has_more_questions(self) -> bool:
        """
        Verificar si hay más preguntas.
        
        Returns:
            bool: True si hay más preguntas, False en caso contrario.
        """
        # Contar cuántas preguntas tiene el quiz actual
        total_questions = self.db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == self.quiz.id
        ).count()
        
        return self.current_question_index < total_questions

    def get_next_question(self) -> Optional[Question]:
        """
        Pasar a la siguiente pregunta.

        Returns:
            Optional[Question]: Siguiente pregunta, o None si no hay más preguntas.
        """
        if not self.has_more_questions():
            return None
        
        # Obtener la siguiente pregunta del quiz
        quiz_question = self.db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == self.quiz.id,
            QuizQuestion.question_index == self.current_question_index
        ).first()
        
        if not quiz_question:
            return None
        
        # Obtener la pregunta completa
        question = self.db.query(Question).filter(
            Question.id == quiz_question.question_id
        ).first()
        
        # Incrementar el índice de pregunta
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
        # Incrementar el contador de preguntas totales
        self.total_questions += 1
        
        # Verificar si la respuesta es correcta
        is_correct = question.is_correct(answer)
        
        # Actualizar el quiz y la pregunta en la base de datos
        quiz_question = self.db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == self.quiz.id,
            QuizQuestion.question_id == question.id
        ).first()
        
        if quiz_question:
            quiz_question.user_answer = answer
            quiz_question.is_correct = is_correct
            quiz_question.answered_at = func.now()
        
        # Actualizar contadores
        if is_correct:
            self.quiz.correct_answers += 1
            self.consecutive_correct += 1
            self.quiz.consecutive_correct += 1
        else:
            self.quiz.incorrect_answers += 1
            self.consecutive_correct = 0
            self.quiz.consecutive_correct = 0
        
        self.db.commit()
        
        # Ajustar la dificultad según el rendimiento
        self.adjust_difficulty()
        
        return is_correct

    def get_score(self) -> dict:
        """
        Muestra la puntuación del jugador.
        
        Returns:
            dict: Diccionario con el total de preguntas, respuestas correctas,
                  respuestas incorrectas, la dificultad actual y la precisión.
        """
        # Obtener la dificultad actual
        difficulty = self.db.query(DifficultyLevel).filter(
            DifficultyLevel.id == self.quiz.current_difficulty_id
        ).first()
        
        total_questions = self.quiz.correct_answers + self.quiz.incorrect_answers
        accuracy = round((self.quiz.correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
        
        return {
            "total_questions": total_questions,
            "correct_answers": self.quiz.correct_answers,
            "incorrect_answers": self.quiz.incorrect_answers,
            "current_difficulty": difficulty.name,
            "accuracy": accuracy
        }
        
    def reset_game(self) -> None:
        """Restaurar el juego al estado inicial."""
        # Marcar el quiz actual como completado
        self.quiz.completed_at = func.now()
        self.db.commit()
        
        # Inicializar un nuevo quiz
        self.total_questions = 0
        self.current_difficulty = 'fácil'
        self.consecutive_correct = 0
        self.current_question_index = 0
        self._initialize_quiz()