from nltk.tokenize import word_tokenize

"""Module for wrapping question database""" 

class Questions(object):
    def __init__(self):
        # TODO: Load question DB into memory (?)
        # TODO: Filter out punctuation?
        self.questions = [word_tokenize(q) for q in  ["hi"]]
        # TODO: Wikipedify answers
        self.answers = ["bye"]
        pass

    def get(self, question_id, word_id):
        if question_id < len(self.questions) and word_id < len(self.questions[question_id]):
            return self.questions[question_id][word_id]
        raise IndexError

    def check_answer(self, question_id, answer):
        return self.answers[question_id] == answer

