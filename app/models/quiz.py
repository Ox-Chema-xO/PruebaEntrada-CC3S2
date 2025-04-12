class Quiz:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0

    def add_question(self, question):
        self.questions.append(question)
    
    def has_more_questions(self):
        return self.current_question_index < len(self.questions)

    def get_next_question(self):
        if self.has_more_questions():
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return question
        return None
