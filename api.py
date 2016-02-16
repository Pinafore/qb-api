#!/usr/bin/env python2
from apiclient import discovery
from csv_questions import CsvQuestions
import flask
from flask import Flask, request
from flask_restful import Resource, Api, abort
import httplib2
from oauth2client import client
import os
import pickle
import threading
import sqlite3
from random import SystemRandom
import signal
import sys
from threading import Lock, Timer
from unidecode import unidecode
from users import UserInfo

"""API module for quiz bowl server. Handles requests from participants."""

server = Flask(__name__)
server.config.from_object('config')
api = Api(server, prefix="/qb-api")
question_db = CsvQuestions("demo.csv")
user_lock = Lock()

user_file = 'users.csv'
user_csv_lock = Lock()
random = SystemRandom()
user_to_key = {}
key_to_user = {}
if os.path.exists(user_file):
    with open(user_file) as f:
        for line in f:
            email, key = line.strip().split(',')
            key = int(key)
            user_to_key[email] = key
            key_to_user[key] = email

user_info = UserInfo('users.db')

# get existing answers so that
for uu, qq in user_info.user_answer_tuples():
    # print("Adding existing answer %i for %i %
    print(qq, type(qq), uu, type(uu))
    question_db.check_answer(qq, uu, "")

# Handle sigint
def handler(signal, frame):
    print("Caught sigint")
    user_info.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def validate_token(token):
    flow = client.flow_from_clientsecrets('client_secrets.json',
                                          scope='https://www.googleapis.com/auth/userinfo.email',
                                          redirect_uri=flask.url_for('urn:ietf:wg:oauth:2.0:oob'))

# OAuth using example from goolge documentation (https://developers.google.com/api-client-library/python/auth/web-app)

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
        if email not in user_to_key:
            key = random.randint(0, 1<<31)
            while key in key_to_users:
                key = random.randint(0, 1<<31)

            user_to_key[email] = key
            key_to_user[key] = email
            user_csv_lock.acquire()
            with open(user_file, 'a+') as f:
                f.write('{},{}\n'.format(email, key))
            user_csv_lock.release()

        return 'Your secret key is: {}'.format(user_to_key[email])

@server.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets('client_secrets.json',
                                          scope='https://www.googleapis.com/auth/userinfo.email',
                                          redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('register'))

def validate_user_key(user_key):
    if user_key not in key_to_user:
        abort(403, message="Unrecognized user: %s" % user_key)


class Question(Resource):
    def post(self, question_id, word_id):
        """Handle word requests"""
        print("Waiting for lock")
        user_id = int(request.form['id'])
        print("Validating ID")
        validate_user_key(user_id)
        user_lock.acquire()
        try:
            word = question_db(question_id, word_id)
        except KeyError:
            user_lock.release()
            abort(400, message="Invalid question or word id.")

        print("Logging query")
        user_info.log_query(user_id, question_id, word_id)
        print("Logged query")

        user_lock.release()
        return {'word': word}


class Next(Resource):
    def get(self, user):
        return {'next': question_db.next(user)}


class NumQs(Resource):
    def get(self):
        return {'count': len(question_db)}


class QLen(Resource):
    def get(self, question_id):
        try:
            return {'length': question_db.qlen(question_id)}
        except KeyError:
            abort(400, message="Invalid question id.")


class Answer(Resource):
    def post(self, question_id):
        """Handle answers"""
        user_id = int(request.form['id'])
        answer = unidecode(request.form['answer'])
        validate_user_key(user_id)
        user_lock.acquire()

        print("Got answer for question %i" % question_id)
        print(user_id)
        # Check answer
        try:
            success = question_db.check_answer(question_id, user_id, answer)
        except KeyError:
            user_lock.release()
            abort(400, message="Invalid question id.")

        first_answer = user_info.store_result(user_id, question_id,
                                              answer, success)
        user_lock.release()
        if first_answer:
            return {'result':success}
        else:
            abort(400, message="An answer has already been submitted for this question.")

api.add_resource(Question, '/question/<int:question_id>/<int:word_id>')
api.add_resource(Answer, '/answer/<int:question_id>')
api.add_resource(NumQs, '/info/count')
api.add_resource(Next, '/info/next/<int:user>')
api.add_resource(QLen, '/info/length/<int:question_id>')

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False)
