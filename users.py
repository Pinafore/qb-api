from collections import defaultdict
from datetime import datetime


"""Module for storing results and other information about participants."""


class UserInfo(object):
    def __init__(self):
        # Dict of lists of (word_id, time) for each word requested. Indexed by question_id.
        self.queries = defaultdict(list)

        # Highest index requested for each question
        # Using neg_one as function instead of lambda to allow pickling
        self.latest = defaultdict(neg_one)

        # Dict of (answer, score, time) tuples indexed by question id.
        self.results = {}

    def log_query(self, question_id, word_id):
        """Log the time of a query from this user"""
        self.queries[question_id].append((word_id, datetime.now()))

        self.latest[question_id] = max(self.latest[question_id], word_id)

    def store_result(self, question_id, answer, success):
        """Store the given answer, score and time for an answered question. Returns the score."""
        if question_id in self.results:
            return None
        #TODO: replace with actual logic
        score = int(success)
        self.results[question_id] = (answer, score, datetime.now())
        return score

def neg_one():
    return -1
