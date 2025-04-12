from typing import List, Optional
from app.models import Question, Quiz

class TriviaManager:
    """
    Clase controladora de la logica del juego Trivia
    """
    def __init__(self):
        self.quiz = Quiz()
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_questions = 0
    
    def load_questions(self) -> None:
        """Cargar preguntas para el juego"""        
        self.quiz.add_question(
            Question(
                "¿Cuál es la capital de Francia?",
                ["Madrid", "Londres", "París", "Berlín"],
                "París"
            )
        )
        self.quiz.add_question(
            Question(
                "¿Quién escribió 'Don Quijote de la Mancha'?",
                ["Gabriel García Márquez", "Miguel de Cervantes", "Jorge Luis Borges", "Federico García Lorca"],
                "Miguel de Cervantes"
            )
        )
        self.quiz.add_question(
            Question(
                "¿Cuál es el océano más grande del mundo?",
                ["Atlántico", "Pacífico", "Índico", "Ártico"],
                "Pacífico"
           )
        )
    
    def has_more_questions(self) -> bool:
        """
        Verificar si hay mas preguntas.
        
        Returns:
            bool: True si hay mas preguntas, False en caso contrario.
        """
        return self.quiz.has_more_questions()

    def get_next_question(self) -> Optional[Question]:
        """
        Pasar a la siguiente pregunta

        Returns:
            Optional[Question]: Siguiente pregunta, o None si no hay mas preguntas
        """        
        return self.quiz.get_next_question()
        
    def answer_question(self, question: Question, answer: str) -> bool:
        """
        Proceso en el cual el jugaor responde la pregunta
        
        Args:
            question (Question): La pregunta a responder
            answer (str): Respuesta del usuario
            
        Returns:
            bool: True si la respuesta es correcta, Falso en caso contrario.
        """
        self.total_questions += 1
        
        if question.is_correct(answer):
            self.correct_answers += 1
            return True
        else:
            self.incorrect_answers += 1
            return False
    
    def get_score(self) -> dict:
        """
        Mostrar la puntuacion del jugador
        
        Returns:
            dict: Diccionario que muestra del total de preguntas, cuantas fueron contestadas correcta e incorrectamnete
        """
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers
        }
    