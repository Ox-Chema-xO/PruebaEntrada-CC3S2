from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.db_models import get_db, create_tables, Question, DifficultyLevel, Quiz, QuizQuestion 
from app.manager_trivia import TriviaManagerDB
from app.consoleUI_trivia import ConsoleUIDB

app = FastAPI(title="Trivia API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Crear en caso no existen
create_tables()

@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {"message": "¡Bienvenido a la API de Trivia!"}

@app.get("/start-game")
def start_game(db: Session = Depends(get_db)):
    """Inicia un nuevo juego y devuelve su ID"""
    trivia_manager = TriviaManagerDB(db)
    return {"quiz_id": trivia_manager.quiz.id}

@app.get("/game/{quiz_id}/next-question")
def get_next_question(quiz_id: int, db: Session = Depends(get_db)):
    """Obtiene la siguiente pregunta del juego"""

    trivia_manager = load_game(quiz_id, db)
    
    if not trivia_manager.has_more_questions():
        return {"message": "No hay más preguntas disponibles"}
    
    question = trivia_manager.get_next_question()
    
    return {
        "question_number": trivia_manager.current_question_index,
        "description": question.description,
        "options": question.options,
        "difficulty": question.difficulty.name
    }

@app.post("/game/{quiz_id}/answer")
def answer_question(
    quiz_id: int, 
    question_data: Dict[str, Any], 
    db: Session = Depends(get_db)
):
    """Procesa la respuesta a una pregunta"""
    trivia_manager = load_game(quiz_id, db)
    
    question_id = question_data.get("question_id")
    answer = question_data.get("answer")
    
    if not question_id or not answer:
        raise HTTPException(status_code=400, detail="Se requiere question_id y answer")
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    is_correct = trivia_manager.answer_question(question, answer)
    
    difficulty_changed = question.difficulty.name != trivia_manager.current_difficulty
    
    return {
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "difficulty_changed": difficulty_changed,
        "new_difficulty": trivia_manager.current_difficulty if difficulty_changed else None
    }

@app.get("/game/{quiz_id}/score")
def get_score(quiz_id: int, db: Session = Depends(get_db)):
    """Obtiene la puntuación actual del juego"""
    trivia_manager = load_game(quiz_id, db)
    
    return trivia_manager.get_score()

def load_game(quiz_id: int, db: Session) -> TriviaManagerDB:
    """Carga un juego existente desde la base de datos"""
    trivia_manager = TriviaManagerDB(db)
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    trivia_manager.quiz = quiz
    trivia_manager.current_question_index = quiz.questions[-1].question_index + 1 if quiz.questions else 0
    
    difficulty = db.query(DifficultyLevel).filter(DifficultyLevel.id == quiz.current_difficulty_id).first()
    trivia_manager.current_difficulty = difficulty.name
    trivia_manager.consecutive_correct = quiz.consecutive_correct
    
    return trivia_manager


if __name__ == "__main__":
    from app.db_models import Question, Quiz, DifficultyLevel, SessionLocal
    
    db = SessionLocal()
    
    try:
        trivia_manager = TriviaManagerDB(db)
        console_ui = ConsoleUIDB(trivia_manager)
        console_ui.run_game()
    finally:
        db.close()