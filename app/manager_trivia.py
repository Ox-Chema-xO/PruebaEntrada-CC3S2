from typing import List, Optional
import random
from app.models import Question, Quiz

class TriviaManager:
    """
    Clase controladora de la lógica del juego Trivia con gestión de niveles de dificultad.
    
    Reglas modificadas:
      - El juego siempre es de 10 preguntas.
      - Se inicia en nivel "fácil".
      - Si el usuario responde 3 preguntas correctas consecutivas, la dificultad sube:
            "fácil" -> "normal" y "normal" -> "difícil".
      - Las respuestas incorrectas no modifican la dificultad.
    """
    def __init__(self):
        self.quiz = Quiz()
        self.total_questions = 0
        self.current_difficulty = 'fácil'  # Nivel inicial modificado a "fácil"
        self.consecutive_correct = 0  # Contador de respuestas correctas consecutivas
        self.correct_count = 0
        self.incorrect_count = 0
        # Diccionario que agrupa las preguntas por dificultad
        self.questions_by_difficulty = {
            'fácil': [],
            'normal': [],
            'difícil': []
        }

    def load_questions(self) -> None:
        """Cargar preguntas para el juego y clasificarlas por dificultad"""
        questions_data = [
            {
                "description": "¿Cuál es la capital de Francia?",
                "options": ["Madrid", "Londres", "París", "Berlín"],
                "correct_answer": "París",
                "difficulty": "fácil"
            },
            {
                "description": "¿Quién escribió 'Don Quijote de la Mancha'?",
                "options": ["Gabriel García Márquez", "Miguel de Cervantes", "Jorge Luis Borges", "Federico García Lorca"],
                "correct_answer": "Miguel de Cervantes",
                "difficulty": "normal"
            },
            {
                "description": "¿Cuál es el océano más grande del mundo?",
                "options": ["Atlántico", "Pacífico", "Índico", "Ártico"],
                "correct_answer": "Pacífico",
                "difficulty": "fácil"
            },
            {
                "description": "¿Cuál es el río más largo del mundo?",
                "options": ["Nilo", "Amazonas", "Misisipi", "Yangtze"],
                "correct_answer": "Amazonas",
                "difficulty": "normal"
            },
            {
                "description": "¿En qué año comenzó la Segunda Guerra Mundial?",
                "options": ["1939", "1940", "1941", "1945"],
                "correct_answer": "1939",
                "difficulty": "normal"
            },
            {
                "description": "¿Cuál es el elemento químico más abundante en la corteza terrestre?",
                "options": ["Hierro", "Oxígeno", "Silicio", "Aluminio"],
                "correct_answer": "Oxígeno",
                "difficulty": "difícil"
            },
            {
                "description": "¿Quién pintó La Mona Lisa?",
                "options": ["Miguel Ángel", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"],
                "correct_answer": "Leonardo da Vinci",
                "difficulty": "fácil"
            },
            {
                "description": "¿Cuál es el planeta más grande del Sistema Solar?",
                "options": ["Tierra", "Júpiter", "Saturno", "Neptuno"],
                "correct_answer": "Júpiter",
                "difficulty": "normal"
            },
            {
                "description": "¿Cuál es la montaña más alta del mundo?",
                "options": ["Monte Everest", "K2", "Monte Kilimanjaro", "Monte McKinley"],
                "correct_answer": "Monte Everest",
                "difficulty": "fácil"
            },
            {
                "description": "¿Qué país tiene la mayor población del mundo?",
                "options": ["India", "Estados Unidos", "China", "Indonesia"],
                "correct_answer": "China",
                "difficulty": "normal"
            },
            {
                "description": "¿Cuál es el símbolo químico del oro?",
                "options": ["Au", "Ag", "Fe", "Cu"],
                "correct_answer": "Au",
                "difficulty": "normal"
            },
            {
                "description": "¿Qué científico propuso la teoría de la relatividad?",
                "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Galileo Galilei"],
                "correct_answer": "Albert Einstein",
                "difficulty": "fácil"
            },
            {
                "description": "¿Cuál es el hueso más largo del cuerpo humano?",
                "options": ["Fémur", "Húmero", "Tibia", "Radio"],
                "correct_answer": "Fémur",
                "difficulty": "normal"
            },
            {
                "description": "¿Cuál es la velocidad de la luz en el vacío?",
                "options": ["300,000 km/s", "150,000 km/s", "200,000 km/s", "250,000 km/s"],
                "correct_answer": "300,000 km/s",
                "difficulty": "difícil"
            },
            {
                "description": "¿En qué año se fundó la ONU?",
                "options": ["1945", "1950", "1939", "1955"],
                "correct_answer": "1945",
                "difficulty": "difícil"
            }
        ]
        
        # Clasificar las preguntas por dificultad
        for q_data in questions_data:
            difficulty = q_data.get("difficulty", "normal")
            question = Question(
                q_data["description"], 
                q_data["options"], 
                q_data["correct_answer"],
                difficulty
            )
            self.questions_by_difficulty[difficulty].append(question)
        
        # Seleccionar las preguntas según la dificultad actual
        self.select_questions_by_difficulty()

    def select_questions_by_difficulty(self) -> None:
        """
        Selecciona preguntas para el quiz basadas exclusivamente en la dificultad actual.
        """
        # Reiniciar el quiz
        self.quiz.clear_questions()
        # Restaurar los contadores de respuestas
        self.quiz.correct_answers = self.correct_count
        self.quiz.incorrect_answers = self.incorrect_count
        
        # Se utiliza únicamente la lista correspondiente a la dificultad actual
        available_questions = self.questions_by_difficulty[self.current_difficulty][:]
        
        random.shuffle(available_questions)
        selected_questions = available_questions[:10]
        
        for question in selected_questions:
            self.quiz.add_question(question)

    
    def adjust_difficulty(self) -> None:
        """
        Ajusta la dificultad en función del rendimiento del jugador.
        Si se contestan 3 preguntas correctas consecutivas, se aumenta el nivel,
        pasando de "fácil" a "normal" y de "normal" a "difícil" (nivel máximo).
        Las respuestas incorrectas no modifican la dificultad.
        """
        if self.consecutive_correct >= 3:
            if self.current_difficulty == 'fácil':
                self.current_difficulty = 'normal'
            elif self.current_difficulty == 'normal':
                self.current_difficulty = 'difícil'
            # Si ya está en "difícil", no se aumenta más
            self.consecutive_correct = 0
            self.select_questions_by_difficulty()

    def has_more_questions(self) -> bool:
        """
        Verificar si hay más preguntas.
        
        Returns:
            bool: True si hay más preguntas, False en caso contrario.
        """
        return self.quiz.has_more_questions()

    def get_next_question(self) -> Optional[Question]:
        """
        Pasar a la siguiente pregunta.

        Returns:
            Optional[Question]: Siguiente pregunta, o None si no hay más preguntas.
        """        
        return self.quiz.get_next_question()
        
    def answer_question(self, question: Question, answer: str) -> bool:
        """
        Procesa la respuesta del jugador a la pregunta,
        actualiza el contador de respuestas consecutivas y ajusta la dificultad.

        Args:
            question (Question): La pregunta a responder.
            answer (str): Respuesta del usuario.
            
        Returns:
            bool: True si la respuesta es correcta, False en caso contrario.
        """
        self.total_questions += 1
        is_correct = self.quiz.answer_question(question, answer)
        
        if is_correct:
            self.consecutive_correct += 1
            self.correct_count += 1
        else:
            # En respuesta incorrecta, se reinicia el contador de respuestas correctas consecutivas
            self.consecutive_correct = 0
            self.incorrect_count += 1
        
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
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.correct_count,
            "incorrect_answers": self.incorrect_count,
            "current_difficulty": self.current_difficulty,
            "accuracy": round((self.quiz.correct_answers / self.total_questions) * 100, 2) if self.total_questions > 0 else 0
        }
        
    def reset_game(self) -> None:
        """Restaurar el juego al estado inicial."""
        self.total_questions = 0
        self.current_difficulty = 'fácil'
        self.consecutive_correct = 0
        self.correct_count = 0
        self.incorrect_count = 0
        # Reiniciar las preguntas según el nivel actual
        self.select_questions_by_difficulty()