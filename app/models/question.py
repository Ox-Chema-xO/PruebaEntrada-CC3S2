class Question:
    def __init__(self, description, options, correct_answer, difficulty='normal'):
        self.description = description
        self.options = options
        self.correct_answer = correct_answer
        self.difficulty = difficulty  

    def is_correct(self, answer):
        return self.correct_answer == answer