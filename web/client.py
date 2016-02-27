import requests


class QbApi(object):
    def __init__(self, user_id):
        """
        Creates an interface object with your provided user id

        user_id -- Your user id, as provided by Workshop organizers
        """
        self.base_url = 'http://127.0.0.1:5000/qb-api'
        self.user_id = user_id

    def get_num_questions(self):
        """
        Returns an integer count of questions
        """
        r = requests.get(self.base_url + '/info/count')
        return int(r.json()['count'])

    def get_question_length(self, question_id):
        """
        Gets the total number of words in a question

        Arguments:
        question_id -- ID of a question
        """
        r = requests.get(self.base_url + '/info/length/%d' % question_id)
        if r.status_code == 200:
            return int(r.json()['length'])
        elif r.status_code == 400:
            raise IndexError(r.json()['message'])
        else:
            raise RuntimeError("Exception:\nStatus: %d\nResponse: %s" %
                               (r.status_code, r.text()))

    def get_word(self, question_id, word_index):
        """
        Provides random access to words in the question.  The maximum word_index
        will determine your overall rating.

        question_id -- ID of a question
        word_index -- The index of a word (starting at zero)
        """
        r = requests.post(self.base_url + '/question/%d/%d' % (question_id, word_index),
                          data={'user_id': self.user_id})
        if r.status_code == 200:
            return r.json()['word']
        elif r.status_code == 400:
            raise IndexError(r.json()['message'])
        else:
            raise RuntimeError("Exception:\nStatus: %d\nResponse: %s" %
                               (r.status_code, r.text))

    def submit_answer(self, question_id, answer):
        """
        Submits an answer to the system.

        question_id -- The ID of the question
        answer -- The answer, as an ASCII string title of Wikipedia page
        """
        r = requests.post(self.base_url + '/answer/%d' % question_id,
                          data={'answer': answer, 'id': self.user_id})
        if r.status_code == 200:
            return r.json()['result']
        elif r.status_code == 400:
            raise ValueError(r.json()['message'])
        else:
            raise RuntimeError("Exception:\nStatus: %d\nResponse: %s" %
                               (r.status_code, r.text()))
