from app.manager_trivia import TriviaManager
from app.consoleUI_trivia import ConsoleUI

def main():
    # Inicializamos trivia_manager con las preguntas
    trivia_manager = TriviaManager()
    trivia_manager.load_questions()
    
    # Inicializamos la consola con trivia_manager
    console_ui = ConsoleUI(trivia_manager)
    
    # Corremos el juego
    console_ui.run_game()

if __name__ == "__main__":
    main()