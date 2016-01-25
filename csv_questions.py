from collections import defaultdict
from csv import DictReader


class CsvQuestions:
    """
    Loads questions from CSV file for random access by server
    """

    def __init__(self, filename):
        self._questions = defaultdict(dict)
        self._answers = {}
        self._guesses = defaultdict(set)

        for ii in DictReader(open(filename)):
            key = ii['id']
            self._answers[key] = ii['answer']
            for jj, ww in enumerate(ii['text'].split()):
                self._questions[key][jj] = ww

    def __len__(self):
        return len(self._questions)

    def qlen(self, question_id):
        return len(self._questions[question_id])

    def next(self, user):
        try:
            return min(x for x in self._questions if not x
                       in self._guesses[user])
        except ValueError:
            return -1

    def check_answer(self, question_id, user, answer):
        self._answers[user].add(question_id)
        return self._answers[question_id] == answer

    def __call__(self, question, word):
        if question in self._questions and word in self._questions[question]:
            return self._questions[question][word]
        else:
            return ""
