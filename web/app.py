"""API module for quiz bowl server. Handles requests from participants."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

server = Flask(__name__)
server.config.from_object(config.BaseConfig)
db = SQLAlchemy(server)

import api
api.create_server()


def run():
    db.create_all()
    server.run(host='0.0.0.0', debug=True)
