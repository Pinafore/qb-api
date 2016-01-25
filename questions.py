from collections import defaultdict
import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
import csv
from itertools import groupby
from nltk.tokenize import word_tokenize
from operator import itemgetter
import os
import pickle
import sqlite3
from threading import Lock
import wikipedia
from wikipedia import DisambiguationError
from wikipedia import PageError
from wikipedia import RedirectError

"""Module for wrapping question database"""


class Questions(object):
    def __init__(self):
        # TODO: Load question DB into memory (?)
        f_name = 'wiki_questions.p'
        if not os.path.exists(f_name):
            conn = sqlite3.connect('./non_naqt.db')
            cur = conn.cursor()
            print("Loading questions database")
            cur.execute('SELECT * FROM text')
            sentences = groupby(cur.fetchall(), key=itemgetter(0))

            # Reduce results of search to just text
            sentences = ((i, map(itemgetter(2), s)) for i,s in sentences)

            # Combine sentences into questions
            q_gen = ((i, " ".join(s)) for i, s in sentences)

            q_dict = {i: word_tokenize(s) for i, s in q_gen}
            # TODO: Wikipedify answers
            # TODO: Save reindexed questions
            cur.execute('SELECT id, answer from questions')
            ans_dict = {i:a for i,a in cur.fetchall()}
            print("Wikipedifying")
            wiki_answers = wikipedify(ans_dict)
            questions = []
            answers = []

            for i,a in wiki_answers.items():
                questions.append(q_dict[i])
                answers.append(a)
            with open(f_name, 'wb') as f:
                pickle.dump((questions, answers), f)
        else:
            with open(f_name, 'rb') as f:
                questions,answers = pickle.load(f)
        self.answers = answers
        self.questions = questions

    def __call__(self, question_id, word_id):
        if question_id < len(self.questions) and word_id < len(self.questions[question_id]):
            return self.questions[question_id][word_id]
        raise IndexError

    def check_answer(self, question_id, answer):
        return self.answers[question_id] == answer

count = 0
# TODO: Serialize so this is a one time cost
def wikipedify(answers):
    num_ans = len(answers)
    lock = Lock()
    def increment():
        global count
        lock.acquire()
        count += 1
        print("Wikipedifying: %d/%d" % (count, num_ans))
        lock.release()

    def getter(ans):
        try:
            increment()
            results = wikipedia.search(query=ans, results=1)
            return results[0] if results else None
        except PageError as e:
            print("PageError: %s" % str(e))
            return None
        except RedirectError as e:
            print("RedirectError: %s" % str(e))
            return None
        except DisambiguationError:
            print("DisambiguationError: %s" % str(e))
            return None
        except Exception as e:
            print("Unknown exception: %s" % str(e))
            return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        ans_futures = {executor.submit(getter, answers[i]): i for i in answers}
        total = 0
        new_answers = {}
        for future in futures.as_completed(ans_futures):
            res = future.result()
            if res is not None:
                new_answers[ans_futures[future]] = res
    return new_answers
