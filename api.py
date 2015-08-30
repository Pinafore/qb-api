from flask import Flask, request
from flask_restful import Resource, Api, abort
from users import UserInfo
from questions import Questions

"""API module for quiz bowl server. Handles requests from participants."""

server = Flask(__name__)
api = Api(server, prefix="/qb-api")
question_db = Questions()
users = {'0':UserInfo()}

def validate_user_id(user_id):
    if user_id not in users:
        abort(403, message="Unrecognized user: %s" % user_id)

class Question(Resource):
    def post(self, question_id, word_id):
        """Handle word requests"""
        user_id = request.form['id']
        validate_user_id(user_id)
        try:
            word = question_db.get(question_id, word_id)
        except IndexError:
            abort(400, message="Invalid question or word id.")

        users[user_id].log_query(question_id, word_id)

        return {'word':word}

class Answer(Resource):
    def post(self, question_id):
        """Handle answers"""
        user_id = request.form['id']
        answer = request.form['answer']
        validate_user_id(user_id)

        # Check answer
        try:
            success = question_db.check_answer(question_id, answer)
        except IndexError:
            abort(400, message="Invalid question id.")
        score = users[user_id].store_result(question_id, answer, success)
        if score:
            return {'score':score}
        else:
            abort(400, message="An answer has already been submitted for this question.")

api.add_resource(Question, '/question/<int:question_id>/<int:word_id>')
api.add_resource(Answer, '/answer/<int:question_id>')

if __name__ == '__main__':
    server.run(debug=True)
