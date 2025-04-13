import pytest
from app.models import Question, Quiz

def test_add_question():
    quiz = Quiz()
    question = Question("Test question, What is the answer?", ["A", "B", "C", "D"], "B")
    quiz.add_question(question)
    assert len(quiz.questions) == 1
    assert quiz.questions[0] == question

def test_get_next_question():
    quiz = Quiz()
    question1 = Question("Q1?", ["A", "B"], "A")
    question2 = Question("Q2?", ["C", "D"], "D")
    quiz.add_question(question1)
    quiz.add_question(question2)
    
    assert quiz.get_next_question() == question1
    assert quiz.get_next_question() == question2
    assert quiz.get_next_question() is None

def test_has_more_questions():
    quiz = Quiz()
    assert not quiz.has_more_questions()
    
    quiz.add_question(Question("Q1?", ["A", "B"], "A"))
    assert quiz.has_more_questions()
    
    quiz.get_next_question()
    assert not quiz.has_more_questions()

def test_answer_question_correct():
    quiz = Quiz()
    question = Question("¿Cuánto es 2+2?", ["3", "4", "5"], "4")
    
    result = quiz.answer_question(question, "4")
    
    assert result is True
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 0

def test_answer_question_incorrect():
    quiz = Quiz()
    question = Question("¿Cuánto es 2+2?", ["3", "4", "5"], "4")
    
    result = quiz.answer_question(question, "3")
    
    assert result is False
    assert quiz.correct_answers == 0
    assert quiz.incorrect_answers == 1

def test_multiple_answers():
    quiz = Quiz()
    question1 = Question("¿Capital de Colombia?", ["Bogota", "Medellin"], "Bogota")
    question2 = Question("¿2 x 3?", ["5", "6", "7"], "6")
    
    quiz.answer_question(question1, "Bogota") 
    quiz.answer_question(question2, "5")       
 
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 1

def test_reset():
    quiz = Quiz()
    quiz.add_question(Question("Q1?", ["A", "B"], "A"))
    quiz.add_question(Question("Q2?", ["C", "D"], "D"))
    
    quiz.correct_answers = 5
    quiz.incorrect_answers = 3
    
    quiz.reset()
    
    assert quiz.current_question_index == 0
    assert quiz.correct_answers == 0
    assert quiz.incorrect_answers == 0