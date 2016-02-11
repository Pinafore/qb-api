from collections import defaultdict
import os
from Queue import Queue
import sqlite3
from threading import Semaphore, Thread, Timer
import time


"""Module for storing results and other information about participants."""


class UserInfo(object):
    def __init__(self, db_file='users.db'):
        self.db_file = db_file
        self.jobs = Queue()
        # Flag to kill reader/writer thread
        self.halt = False
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            cur.execute('CREATE TABLE queries(userid integer, qid integer, wid integer, time real, PRIMARY KEY (userid, qid, wid))')
            cur.execute('CREATE TABLE latest(userid integer, qid integer, wid integer, PRIMARY KEY (userid, qid))')
            cur.execute('CREATE TABLE results(userid integer, qid integer, guess text, correct text, time real, PRIMARY KEY (userid, qid))')
            conn.commit()
            conn.close()
        self.run_thread = Thread(target=self.runner)
        self.run_thread.start()
        self.commit_period = 600
        self.commit_timer = Timer(self.commit_period, self.committer)
        self.commit_timer.start()

    def shutdown(self):
        self.commit_timer.cancel()
        self.halt = True
        self.jobs.put(None)
        self.run_thread.join()

    def runner(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        while not self.halt:
            print("Waiting for job")
            t = self.jobs.get()
            if t is None:
                conn.commit()
                continue
            else:
                job, res = t
                print("Executing: %s" % str(job))
                cur.execute(*job)
                res.content = cur.fetchall()
                res.notify()

    def user_answer_tuples(self):
        res = self.execute('SELECT userid, qid FROM results')
        for uu, qq in res:
            yield uu, qq

    def committer(self):
        self.jobs.put(None)
        Timer(self.commit_period, self.committer).start()

    # Wrapper for passing jobs into the sqlite thread
    def execute(self, *job):
        res = UserInfo.Result()
        self.jobs.put((job, res))
        res.wait()
        return res.content

    def log_query(self, user_id, question_id, word_id):
        """Log the time of a query from this user"""
        res = self.execute('SELECT wid FROM latest WHERE userid=? and qid=?', (user_id, question_id))
        if not res or word_id > res[0][0]:
            curr_time = time.time()
            self.execute('INSERT INTO queries (userid, qid, wid, time) VALUES (?,?,?,?)',\
                            (user_id, question_id, word_id, curr_time))
            self.execute('INSERT or REPLACE INTO latest (userid, qid, wid) VALUES (?,?,?)',\
                            (user_id, question_id, word_id))

    def store_result(self, user_id, question_id, answer, success):
        """Store the given answer, score and time for an answered question. Returns the score."""
        res = self.execute('SELECT * FROM results WHERE userid = ? and qid = ?', (user_id, question_id))
        if res:
            return False
        curr_time = time.time()
        self.execute('INSERT INTO results (userid, qid, guess, correct, time) VALUES (?,?,?,?,?)',\
                        (user_id, question_id, answer, str(success), curr_time))
        return True

    # Wrapper for sqlite3 results
    class Result(object):
        def __init__(self, content=None):
            self.content = content
            self.sem = Semaphore(0)

        def wait(self):
            self.sem.acquire()

        def notify(self):
            self.sem.release()
