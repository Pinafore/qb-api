from flask import Flask, request
from flask_restful import Resource, Api, abort
import os
import pickle
import threading
from threading import Lock, Timer
from users import UserInfo
from questions import Questions

"""API module for quiz bowl server. Handles requests from participants."""

_SERIALIZE_PERIOD = 10
server = Flask(__name__)
api = Api(server, prefix="/qb-api")
question_db = Questions()
user_lock = Lock()
#TODO: Replace pickling with another storage method
if os.path.exists('userdata.p'):
    with open('userdata.p', 'rb') as f:
        users = pickle.load(f)
else:
    users = {'0':UserInfo()}

def serializer():
    user_lock.acquire()
    with open("userdata.p", "wb") as f:
        pickle.dump(users, f)
    user_lock.release()
    Timer(_SERIALIZE_PERIOD, serializer).start()
serializer()

def validate_user_id(user_id):
    if user_id not in users:
        abort(403, message="Unrecognized user: %s" % user_id)

class Question(Resource):
    def post(self, question_id, word_id):
        """Handle word requests"""
        print("Waiting for lock")
        user_lock.acquire()
        user_id = request.form['id']
        print("Validating ID")
        validate_user_id(user_id)
        try:
            word = question_db.get(question_id, word_id)
        except IndexError:
            user_lock.release()
            abort(400, message="Invalid question or word id.")

        print("Logging query")
        users[user_id].log_query(question_id, word_id)
        print("Logged query")

        user_lock.release()
        return {'word':word}

class Answer(Resource):
    def post(self, question_id):
        """Handle answers"""
        user_id = request.form['id']
        answer = request.form['answer']
        user_lock.acquire()
        validate_user_id(user_id)

        # Check answer
        try:
            success = question_db.check_answer(question_id, answer)
        except IndexError:
            user_lock.release()
            abort(400, message="Invalid question id.")

        score = users[user_id].store_result(question_id, answer, success)
        user_lock.release()
        if score is not None:
            return {'score':score}
        else:
            abort(400, message="An answer has already been submitted for this question.")

api.add_resource(Question, '/question/<int:question_id>/<int:word_id>')
api.add_resource(Answer, '/answer/<int:question_id>')

if __name__ == '__main__':
    server.run()
