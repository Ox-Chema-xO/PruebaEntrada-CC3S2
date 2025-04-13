import pytest
from app.models import Question

def test_question_creation():
    question = Question("What is 2 + 2?", ["1", "2", "3", "4"], "4")
    assert question.description == "What is 2 + 2?"
    assert question.options == ["1", "2", "3", "4"]
    assert question.correct_answer == "4"

def test_correct_answer():
    question = Question("Capital of France?", ["London", "Berlin", "Paris", "Rome"], "Paris")
    assert question.is_correct("Paris")

def test_incorrect_answer():
    question = Question("Capital of France?", ["London", "Berlin", "Paris", "Rome"], "Paris")
    assert not question.is_correct("Berlin") 

