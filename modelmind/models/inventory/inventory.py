class Inventory:
    def __init__(self, questions: list):
        self.questions = questions

    def add_question(self, question):
        self.questions.append(question)

    def remove_question(self, question):
        self.questions.remove(question)

    def edit_question(self, question, new_question):
        self.questions[self.questions.index(question)] = new_question

    def list_questions(self):
        self.questions

    def get_question(self, question):
        return self.questions[self.questions.index(question)]

    def change_visibility(self):
        pass

    def start_session(self):
        pass

    def end_session(self):
        pass
