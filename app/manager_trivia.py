from typing import List, Optional
import random
from app.models import Question, Quiz

class TriviaManager:
    """
    Clase controladora de la lógica del juego Trivia
    Ahora incluye gestión de niveles de dificultad
    """
    def __init__(self):
        self.quiz = Quiz()
        self.total_questions = 0
        self.current_difficulty = 'normal'  # Dificultad inicial
        self.consecutive_correct = 0  # Contador de respuestas correctas consecutivas
        self.consecutive_incorrect = 0  # Contador de respuestas incorrectas consecutivas
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
        
        # Seleccionar las primeras preguntas según la dificultad inicial
        self._select_questions_by_difficulty()

    def _select_questions_by_difficulty(self) -> None:
        """
        Selecciona preguntas para el quiz basadas en la dificultad actual
        """
        # Limpiar completamente las preguntas actuales y reiniciar contadores
        self.quiz.clear_questions()
        
        # Seleccionar preguntas de la dificultad actual y adyacentes
        available_questions = []
        
        # Siempre incluimos algunas preguntas de la dificultad actual
        if self.questions_by_difficulty[self.current_difficulty]:
            available_questions.extend(self.questions_by_difficulty[self.current_difficulty])
        
        # Si la dificultad actual es 'normal', añadimos algunas fáciles y difíciles
        if self.current_difficulty == 'normal':
            available_questions.extend(self.questions_by_difficulty['fácil'])
            available_questions.extend(self.questions_by_difficulty['difícil'])
        # Si es 'fácil', añadimos algunas normales
        elif self.current_difficulty == 'fácil':
            available_questions.extend(self.questions_by_difficulty['normal'])
        # Si es 'difícil', añadimos algunas normales
        elif self.current_difficulty == 'difícil':
            available_questions.extend(self.questions_by_difficulty['normal'])
        
        # Mezclar las preguntas disponibles y seleccionar hasta 10
        random.shuffle(available_questions)
        selected_questions = available_questions[:10]
        
        # Añadir las preguntas seleccionadas al quiz
        for question in selected_questions:
            self.quiz.add_question(question)   
    
    def adjust_difficulty(self) -> None:
        """
        Ajusta la dificultad según el rendimiento del jugador
        """
        # Si el jugador acierta varias preguntas consecutivas, aumentamos la dificultad
        if self.consecutive_correct >= 3:
            if self.current_difficulty == 'fácil':
                self.current_difficulty = 'normal'
            elif self.current_difficulty == 'normal':
                self.current_difficulty = 'difícil'
            self.consecutive_correct = 0
            self._select_questions_by_difficulty()
        
        # Si el jugador falla varias preguntas consecutivas, reducimos la dificultad
        elif self.consecutive_incorrect >= 2:
            if self.current_difficulty == 'difícil':
                self.current_difficulty = 'normal'
            elif self.current_difficulty == 'normal':
                self.current_difficulty = 'fácil'
            self.consecutive_incorrect = 0
            self._select_questions_by_difficulty()

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
            Optional[Question]: Siguiente pregunta, o None si no hay más preguntas
        """        
        return self.quiz.get_next_question()
        
    def answer_question(self, question: Question, answer: str) -> bool:
        """
        Proceso en el cual el jugador responde la pregunta
        Actualiza contadores de respuestas consecutivas y ajusta la dificultad
        
        Args:
            question (Question): La pregunta a responder
            answer (str): Respuesta del usuario
            
        Returns:
            bool: True si la respuesta es correcta, Falso en caso contrario.
        """
        self.total_questions += 1
        is_correct = self.quiz.answer_question(question, answer)
        
        if is_correct:
            self.consecutive_correct += 1
            self.consecutive_incorrect = 0
        else:
            self.consecutive_incorrect += 1
            self.consecutive_correct = 0
        
        # Ajustar la dificultad basada en el rendimiento
        self.adjust_difficulty()
        
        return is_correct

    def get_score(self) -> dict:
        """
        Mostrar la puntuación del jugador
        
        Returns:
            dict: Diccionario que muestra del total de preguntas, cuántas fueron contestadas correcta e incorrectamente,
                 y la dificultad actual
        """
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.quiz.correct_answers,
            "incorrect_answers": self.quiz.incorrect_answers,
            "current_difficulty": self.current_difficulty,
            "accuracy": round((self.quiz.correct_answers / self.total_questions) * 100, 2) if self.total_questions > 0 else 0
        }
        
    def reset_game(self) -> None:
        """Restaurar el juego"""
        self.total_questions = 0
        self.current_difficulty = 'normal'
        self.consecutive_correct = 0
        self.consecutive_incorrect = 0
        # Limpia las preguntas y reinicia los contadores
        self._select_questions_by_difficulty()