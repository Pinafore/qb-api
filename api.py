#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api, abort
import os
import pickle
import threading
import sqlite3
from questions import Questions
import signal
import sys
from threading import Lock, Timer
from users import UserInfo

"""API module for quiz bowl server. Handles requests from participants."""

server = Flask(__name__)
api = Api(server, prefix="/qb-api")
question_db = Questions()
user_lock = Lock()
users = set()
# Get list of user ids
with open('users') as f:
    for line in f:
        users.add(line.strip())

user_info = UserInfo('users.db')

# Handle sigint
def handler(signal, frame):
    print("Caught sigint")
    user_info.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def validate_user_id(user_id):
    if user_id not in users:
        abort(403, message="Unrecognized user: %s" % user_id)

class Question(Resource):
    def post(self, question_id, word_id):
        """Handle word requests"""
        print("Waiting for lock")
        user_id = request.form['id']
        print("Validating ID")
        validate_user_id(user_id)
        user_lock.acquire()
        try:
            word = question_db.get(question_id, word_id)
        except IndexError:
            user_lock.release()
            abort(400, message="Invalid question or word id.")

        print("Logging query")
        user_info.log_query(user_id, question_id, word_id)
        print("Logged query")

        user_lock.release()
        return {'word':word}

class Answer(Resource):
    def post(self, question_id):
        """Handle answers"""
        user_id = request.form['id']
        answer = request.form['answer']
        validate_user_id(user_id)
        user_lock.acquire()
        # Check answer
        try:
            success = question_db.check_answer(question_id, answer)
        except IndexError:
            user_lock.release()
            abort(400, message="Invalid question id.")

        score = user_info.store_result(user_id, question_id, answer, success)
        user_lock.release()
        if score is not None:
            return {'score':score}
        else:
            abort(400, message="An answer has already been submitted for this question.")

api.add_resource(Question, '/question/<int:question_id>/<int:word_id>')
api.add_resource(Answer, '/answer/<int:question_id>')

if __name__ == '__main__':
    server.run(debug=True)
