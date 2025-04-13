from typing import List, Optional
from app.models import Question, Quiz

class TriviaManager:
    """
    Clase controladora de la logica del juego Trivia
    """
    def __init__(self):
        self.quiz = Quiz()
        self.total_questions = 0

    def load_questions(self) -> None:
        """Cargar preguntas para el juego"""
        questions_data = [
            {
                "description": "¿Cuál es la capital de Francia?",
                "options": ["Madrid", "Londres", "París", "Berlín"],
                "correct_answer": "París"
            },
            {
                "description": "¿Quién escribió 'Don Quijote de la Mancha'?",
                "options": ["Gabriel García Márquez", "Miguel de Cervantes", "Jorge Luis Borges", "Federico García Lorca"],
                "correct_answer": "Miguel de Cervantes"
            },
            {
                "description": "¿Cuál es el océano más grande del mundo?",
                "options": ["Atlántico", "Pacífico", "Índico", "Ártico"],
                "correct_answer": "Pacífico"
            },
            {
                "description": "¿Cuál es el río más largo del mundo?",
                "options": ["Nilo", "Amazonas", "Misisipi", "Yangtze"],
                "correct_answer": "Amazonas"
            },
            {
                "description": "¿En qué año comenzó la Segunda Guerra Mundial?",
                "options": ["1939", "1940", "1941", "1945"],
                "correct_answer": "1939"
            },
            {
                "description": "¿Cuál es el elemento químico más abundante en la Tierra?",
                "options": ["Hierro", "Oxígeno", "Silicio", "Aluminio"],
                "correct_answer": "Oxígeno"
            },
            {
                "description": "¿Quién pintó La Mona Lisa?",
                "options": ["Miguel Ángel", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"],
                "correct_answer": "Leonardo da Vinci"
            },
            {
                "description": "¿Cuál es el planeta más grande del Sistema Solar?",
                "options": ["Tierra", "Júpiter", "Saturno", "Neptuno"],
                "correct_answer": "Júpiter"
            },
            {
                "description": "¿Cuál es la montaña más alta del mundo?",
                "options": ["Monte Everest", "K2", "Monte Kilimanjaro", "Monte McKinley"],
                "correct_answer": "Monte Everest"
            },
            {
                "description": "¿Qué país tiene la mayor población del mundo?",
                "options": ["India", "Estados Unidos", "China", "Indonesia"],
                "correct_answer": "China"
            }
        ]
        for q_data in questions_data:
            self.quiz.add_question(
                Question(q_data["description"], q_data["options"], q_data["correct_answer"])
            )

    def has_more_questions(self) -> bool:
        """
        Verificar si hay más preguntas.
        
        Returns:
            bool: True si hay más preguntas, False en caso contrario.
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
        return self.quiz.answer_question(question, answer)
        

    def get_score(self) -> dict:
        """
        Mostrar la puntuacion del jugador
        
        Returns:
            dict: Diccionario que muestra del total de preguntas, cuantas fueron contestadas correcta e incorrectamnete
        """
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.quiz.correct_answers,
            "incorrect_answers": self.quiz.incorrect_answers
        }
    def reset_game(self) -> None:
        """Restaurar el juego"""
        self.quiz.reset()
        self.quiz.correct_answers= 0
        self.quiz.incorrect_answers = 0
        self.total_questions = 0   