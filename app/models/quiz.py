class Quiz:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

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
    
    def answer_question(self, question, answer):
        if question.is_correct(answer):
            self.correct_answers += 1
            return True
        else:
            self.incorrect_answers += 1
            return False
            
    def reset(self):
        self.current_question_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        
    def clear_questions(self):
        self.questions = []
        self.reset()