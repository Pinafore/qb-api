import string
import random
import httplib2

import flask
from flask import jsonify, request
from flask_restful import Resource, Api, abort, reqparse

from oauth2client import client
from operator import itemgetter
from apiclient import discovery

from database import QuizBowl
from app import server


def generate_api_key():
    return ''.join(random.choice(string.ascii_letters) for i in range(64))


@server.route('/status')
def alive():
    return jsonify(status='OK')


# OAuth using example from google documentation
# (https://developers.google.com/api-client-library/python/auth/web-app)
@server.route('/register')
def register():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))

    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        account_service = discovery.build('oauth2', 'v2', http=http_auth)
        email = account_service.userinfo().get().execute()['email']
        api_key = generate_api_key()
        user = QuizBowl.create_user(email, api_key)
        return jsonify(**user)

@server.route('/')
def leaderboard():
    scores = QuizBowl.get_scores()

    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    num_questions = QuizBowl.num_questions(fold='dev')
    num_test_questions = QuizBowl.num_questions(fold='test')
    return flask.render_template(
        'leaderboard.html',
        scores=sorted_scores,
        num_questions=num_questions,
        fold='dev',
        num_test_questions=num_test_questions
    )


@server.route('/qb-api/v1/questions')
def list_questions():
    return jsonify(**QuizBowl.list_questions())


@server.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('data/client_secrets.json',
                                          scope='https://www.googleapis.com/auth/userinfo.email',
                                          redirect_uri=flask.url_for('oauth2callback',
                                                                     _external=True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('register'))


def check_auth(user_id, api_key):
    if not QuizBowl.check_auth(user_id, api_key):
        abort(401)


class StatusList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('api_key', type=str)
        parser.add_argument('user_id', type=int)
        args = parser.parse_args()
        check_auth(args['user_id'], args['api_key'])
        return jsonify({'question_statuses': QuizBowl.question_statuses(args['user_id'])})


class Question(Resource):
    def post(self, question_id, position):
        """Handle word requests"""
        print("Question_id: {} Position: {}".format(repr(question_id), repr(position)))
        user_id = int(request.form['user_id'])
        api_key = request.form['api_key']
        check_auth(user_id, api_key)
        word = QuizBowl.handle_word_request(user_id, question_id, position)
        return jsonify({'word': word})


class NumQs(Resource):
    def get(self):
        return jsonify({'count': QuizBowl.num_questions()})


class QLen(Resource):
    def get(self, question_id):
        return jsonify({'length': QuizBowl.question_length(question_id)})


class Answer(Resource):
    def post(self, question_id):
        """Handle answers"""
        user_id = int(request.form['user_id'])
        api_key = request.form['api_key']
        guess = request.form['guess']
        check_auth(user_id, api_key)
        answer, correct = QuizBowl.submit_guess(user_id, question_id, guess)

        return jsonify({'correct': correct, 'answer': answer})


def create_server():
    api = Api(server, prefix="/qb-api/v1")
    api.add_resource(Question, '/question/<int:question_id>/<int:position>')
    api.add_resource(Answer, '/answer/<int:question_id>')
    api.add_resource(NumQs, '/info/count')
    api.add_resource(QLen, '/info/length/<int:question_id>')
