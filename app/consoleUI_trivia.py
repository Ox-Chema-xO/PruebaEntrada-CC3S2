from app.models import Question
from app.manager_trivia import TriviaManager

class ConsoleUI:
    """
    ConsoleUI maneja la interfaz de usuario para el juego. 
    """   
    def __init__(self, trivia_manager: TriviaManager):
        self.trivia_manager = trivia_manager
    
    def display_welcome(self) -> None:
        """Mostrar mensaje de bienvenida con las reglas del juego."""
        print("="*50)
        print("Bienvenido al juego de trivia!")
        print("="*50)
        print("Responde las siguientes preguntas seleccionando el número de la opción correcta.")
        print()
    
    def display_question(self, question: Question, question_number: int) -> None:
        """
        Mostrar las preguntas
        
        Args:
            question (Question): La pregunta a respoder
            question_number (int): El numero de la pregunta
        """
        print(f"\nPregunta {question_number}: {question.description}")
        for i, option in enumerate(question.options, 1):
            print(f"{i}) {option}")
    
    def get_user_answer(self, question: Question) -> str:
        """
        Obtener la respuesta del jugador (indice de la respuesta)
        
        Args:
            question (Question): La pregunta actual con las opciones a elegir
            
        Returns:
            str: Indice de la respuesta del jugador
        """
        while True:
            try:
                answer_index = int(input("\nTu respuesta (número): ")) - 1
                if 0 <= answer_index < len(question.options):
                    return question.options[answer_index]
                else:
                    print(f"Por favor, ingresa un número entre 1 y {len(question.options)}.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
    
    def display_answer_result(self, is_correct: bool, correct_answer: str) -> None:
        """
        Mostrar si la respuesta es correcta o incorrecta.
        
        Args:
            is_correct (bool): True, si la respuesta es correcta , False en caso contrario
            correct_answer (str): La respuesta correcta.
        """
        if is_correct:
            print("¡Correcto!")
        else:
            print(f"Incorrecto. La respuesta correcta era: {correct_answer}")
    
    def display_game_over(self) -> None:
        """Mostrar la puntuacion del jugador."""
        score = self.trivia_manager.get_score()
        
        print("\n" + "="*50)
        print("Juego terminado. Aquí está tu puntuación:")
        print("="*50)
        print(f"Preguntas contestadas: {score['total_questions']}")
        print(f"Respuestas correctas: {score['correct_answers']}")
        print(f"Respuestas incorrectas: {score['incorrect_answers']}")
        print("="*50)
        print("¡Gracias por jugar!")
    
    def run_game(self) -> None:
        """Correr el juego de trivia mediante la interfaz de usuario (consola)"""
        self.display_welcome()  
        question_number = 1 

        while self.trivia_manager.has_more_questions():
            question = self.trivia_manager.get_next_question()
            if question:
                self.display_question(question, question_number)
                user_answer = self.get_user_answer(question)
                is_correct = self.trivia_manager.answer_question(question, user_answer)
                self.display_answer_result(is_correct, question.correct_answer)
                question_number += 1
                
        self.display_game_over()