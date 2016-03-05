from datetime import datetime
from csv import DictReader

from flask import abort

from app import db


LIMITS = False


class QuestionStatus(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    position = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Result(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    position = db.Column(db.Integer)
    guess = db.Column(db.String)
    correct = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    question_statuses = db.relationship('QuestionStatus')
    queries = db.relationship('Query')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qb_id = db.Column(db.Integer)
    words = db.relationship('Word', backref='question')
    answer = db.Column(db.String, nullable=False)
    fold = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class QuizBowl:
    @staticmethod
    def user_answer_pairs():
        return Result.query.all()

    @staticmethod
    def handle_word_request(user_id, question_id, position):
        word = Word.query.filter_by(question_id=question_id, position=position).first()
        if word is None:
            abort(400, message='Invalid question id and position')
        status = QuestionStatus.query.filter_by(
            user_id=user_id, question_id=question_id).first()
        if status:
            if status.position < word.position:
                status.position = word.position
                status.word_id = word.id
                status.datetime = datetime.now()
        else:
            db.session.add(
                QuestionStatus(user_id=user_id,
                               question_id=question_id,
                               position=word.position,
                               word_id=word.id))
        db.session.add(
            Query(user_id=user_id, question_id=question_id, word_id=word.id)
        )
        db.session.commit()
        return {'position': word.position, 'question_id': word.question_id, 'text': word.text}

    @staticmethod
    def submit_guess(user_id, question_id, guess):
        result = Result.query.filter_by(user_id=user_id, question_id=question_id).first()
        if result is not None and LIMITS:
            abort(400, 'Answered question already')

        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            abort(400, 'Question does not exist')
        correct = question.answer == guess
        status = QuestionStatus.query.filter_by(user_id=user_id, question_id=question_id).first()
        if result is None:
            result = Result(
                user_id=user_id,
                question_id=question_id,
                guess=guess,
                correct=correct,
                position=status.position,
                word_id=status.word_id)
        else:
            result.guess = guess
            result.correct = correct
            result.position = status.position
            result.word_id = status.word_id
        db.session.add(result)
        db.session.commit()
        return question.answer, correct

    @staticmethod
    def store_result(user_id, question_id, answer, correct):
        result = Result.query.filter_by(user_id=user_id, question_id=question_id).count()
        if result == 0:
            db.session.add(
                Result(user_id=user_id, question_id=question_id, answer=answer, correct=correct))
            db.session.commit()

    @staticmethod
    def create_user(email, api_key):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            abort(400, "User with that email exists, api key is {0}, user_id is {1}".format(user.api_key, user.id))
        user = User(email=email, api_key=api_key)
        db.session.add(user)
        db.session.commit()
        return {'email': email, 'api_key': api_key, 'id': user.id}

    @staticmethod
    def check_auth(user_id, api_key):
        return User.query.filter_by(id=user_id, api_key=api_key).count() == 1

    @staticmethod
    def num_questions():
        return Question.query.count()

    @staticmethod
    def question_length(question_id):
        question = Question.query.filter_by(id=question_id).first()
        if question:
            return len(question.words)
        else:
            abort(400, 'Invalid question')

    @staticmethod
    def question_statuses(user_id):
        return QuestionStatus.query.filter_by(user_id=user_id).all()

    @staticmethod
    def list_questions():
        questions = Question.query.all()
        question_list = map(lambda q: {'id': q.id, 'word_count': len(q.words)}, questions)
        return {'questions': list(question_list)}


def load_questions(filename='data/demo.csv'):
    Question.query.delete()
    with open(filename) as f:
        questions = DictReader(f)
        for q in questions:
            q_id = int(q['id'])
            question = Question(qb_id=q_id, answer=q['answer'], fold='dev')
            for i, word in enumerate(q['text'].split()):
                question.words.append(Word(text=word, position=i))
            db.session.add(question)
        db.session.commit()
