from app.models import Question
from app.manager_trivia import TriviaManager
import os
import time

class ConsoleUI:
    """
    ConsoleUI maneja la interfaz de usuario para el juego. 
    Versión mejorada con mejor formateo y presentación
    """   
    def __init__(self, trivia_manager: TriviaManager):
        self.trivia_manager = trivia_manager
        #Limpiar pantalla al inicio
        self._clear_screen()
    
    def _clear_screen(self):
        """Limpiar la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self) -> None:
        """Mostrar mensaje de bienvenida con las reglas del juego."""
        print("\n" + "="*60)
        print("|" + " "*58 + "|")
        print("|      BIENVENIDO AL JUEGO DE TRIVIA |")
        print("|" + " "*58 + "|")
        print("="*60)
        
        print("\n>> INSTRUCCIONES:")
        print("  - Responde las preguntas seleccionando el número de la opción correcta.")
        print("  - El juego ajustará la dificultad según tu rendimiento.")
        print(f"  - Nivel inicial: {self.trivia_manager.current_difficulty.upper()}")
        print("  - ¡Responde correctamente para desbloquear preguntas más difíciles!")
        
        print("\n>> Presiona ENTER para comenzar la aventura...")
        input()
        self._clear_screen()
    
    def display_question(self, question: Question, question_number: int, max_questions: int) -> None:
        """
        Mostrar las preguntas con mejor formato
        
        Args:
            question (Question): La pregunta a responder
            question_number (int): El número de la pregunta
        """
        # Mostrar progreso y dificultad
        total_questions = len(self.trivia_manager.quiz.questions)
        
        # Crear un borde superior
        print("\n" + "-"*60)
         # Mostrar información de la pregunta con el total correcto
        print(f"| PREGUNTA {question_number}/{max_questions} | DIFICULTAD: {question.difficulty.upper()} |")
        
        # Mostrar información de la pregunta
        #print(f"| PREGUNTA {question_number}/{total_questions} | DIFICULTAD: {question.difficulty.upper()} |")
        
        # Crear un separador
        print("-"*60)
        
        # Mostrar la descripción de la pregunta con formato
        print(f"\n>> {question.description}")
        
        # Mostrar opciones con mejor formato
        print("\nOpciones:")
        for i, option in enumerate(question.options, 1):
            print(f"  [{i}] {option}")
    
    def get_user_answer(self, question: Question) -> str:
        """
        Obtener la respuesta del jugador (índice de la respuesta)
        
        Args:
            question (Question): La pregunta actual con las opciones a elegir
            
        Returns:
            str: Índice de la respuesta del jugador
        """
        while True:
            try:
                answer_index = int(input("\n>> Tu respuesta (número): ")) - 1
                if 0 <= answer_index < len(question.options):
                    return question.options[answer_index]
                else:
                    print(f"\n! Por favor, ingresa un número entre 1 y {len(question.options)}.")
            except ValueError:
                print("\n! Por favor, ingresa un número válido.")
    
    def display_answer_result(self, is_correct: bool, correct_answer: str) -> None:
        """
        Mostrar si la respuesta es correcta o incorrecta.
        
        Args:
            is_correct (bool): True, si la respuesta es correcta , False en caso contrario
            correct_answer (str): La respuesta correcta.
        """
        if is_correct:
            print("\n" + "*"*60)
            print("*" + " "*19 + "¡RESPUESTA CORRECTA!" + " "*19 + "*")
            print("*"*60)
        else:
            print("\n" + "-"*60)
            print("- INCORRECTO. La respuesta correcta era: " + correct_answer)
            print("-"*60)
        
        # Añadir pequeña pausa para que el usuario pueda leer el resultado
        time.sleep(1.5)
        self._clear_screen()
    
    def display_difficulty_change(self, new_difficulty: str) -> None:
        """
        Mostrar cuando cambia la dificultad
        
        Args:
            new_difficulty (str): La nueva dificultad
        """
        print("\n" + "!"*60)
        print("!" + " "*10 + f"¡LA DIFICULTAD HA CAMBIADO A {new_difficulty.upper()}!" + " "*10 + "!")
        print("!" + " "*10 + "Se han seleccionado nuevas preguntas adecuadas" + " "*10 + "!")
        print("!"*60)
        time.sleep(1.5)
    
    def display_game_over(self) -> None:
        """Mostrar la puntuación del jugador con formato mejorado."""
        score = self.trivia_manager.get_score()
        
        print("\n" + "="*60)
        print("|" + " "*58 + "|")
        print("|" + " "*20 + "FIN DEL JUEGO" + " "*26 + "|")
        print("|" + " "*58 + "|")
        print("="*60)
        
        print("\n>> RESUMEN DE TU PARTIDA:")
        print(f"  • Preguntas contestadas: {score['total_questions']}")
        print(f"  • Respuestas correctas: {score['correct_answers']}")
        print(f"  • Respuestas incorrectas: {score['incorrect_answers']}")
        
        # Mostrar precisión y evaluación del rendimiento
        accuracy = score['accuracy']
        print(f"\n>> PRECISIÓN: {accuracy}%")
        
        print("\n>> EVALUACIÓN:")
        if accuracy >= 90:
            print("  ¡EXCELENTE! Eres un maestro de la trivia. 🏆")
        elif accuracy >= 70:
            print("  ¡MUY BIEN! Tienes un buen conocimiento general. 🎓")
        elif accuracy >= 50:
            print("  ¡BIEN HECHO! Pero hay espacio para mejorar. 📚")
        else:
            print("  Necesitas practicar más. ¡No te rindas! 💪")
        
        print(f"\n>> NIVEL DE DIFICULTAD ALCANZADO: {score['current_difficulty'].upper()}")
        
        # Borde final
        print("\n" + "="*60)
        print("|" + " "*13 + "¡GRACIAS POR JUGAR!" + " "*26 + "|")
        print("|" + " "*8 + "Vuelve pronto para más desafíos." + " "*15 + "|")
        print("="*60)
    
    def display_progress(self) -> None:
        """Mostrar el progreso actual del juego"""
        score = self.trivia_manager.get_score()
        total_questions = len(self.trivia_manager.quiz.questions)
        current_question = self.trivia_manager.quiz.current_question_index
        
        print("\n" + "-"*60)
        print(">> PROGRESO ACTUAL:")
        print(f"  • Pregunta: {current_question}/{total_questions}")
        print(f"  • Correctas: {score['correct_answers']}")
        print(f"  • Incorrectas: {score['incorrect_answers']}")
        print(f"  • Dificultad: {score['current_difficulty'].upper()}")
        print("-"*60)
 
    def run_game(self) -> None:
        self.display_welcome()
        question_number = 1
        max_questions = 10  
        previous_difficulty = self.trivia_manager.current_difficulty

        while question_number <= max_questions and self.trivia_manager.has_more_questions():
            question = self.trivia_manager.get_next_question()
            if question:
                self.display_question(question, question_number, max_questions)
                user_answer = self.get_user_answer(question)
                is_correct = self.trivia_manager.answer_question(question, user_answer)
                self.display_answer_result(is_correct, question.correct_answer)
                
                if previous_difficulty != self.trivia_manager.current_difficulty:
                    self.display_difficulty_change(self.trivia_manager.current_difficulty)
                    previous_difficulty = self.trivia_manager.current_difficulty
                
                if question_number % 3 == 0 and question_number < max_questions:
                    self.display_progress(question_number, max_questions)
                
                question_number += 1
        self.display_game_over()