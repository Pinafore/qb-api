import requests

class QbApi(object):
    # uid is your user_id
    def __init__(self, uid):
        self.base_url = 'http://127.0.0.1:5000/qb-api'
        self.uid = uid

    # Call this to get a count of questions
    def get_num_questions(self):
        r = requests.get(self.base_url + '/info/count')
        return r.json()['count']

    # Call this to get the length of a particular question
    def get_question_length(self, question_id):
        r = requests.get(self.base_url + '/info/length/%d' % question_id)
        if r.status_code == 200:
            return r.json()['length']
        elif r.status_code == 400:
            raise IndexError(r.json()['message'])
        else:
            raise RuntimeError("Unexpected exception:\nStatus code: %d\nResponse: %s" % (r.status_code, r.text()))

    # Call this to get a word of a question
    def get_word(self, question_id, word_index):
        r = requests.post(self.base_url + '/question/%d/%d' % (question_id, word_index),\
                            data = {'id':self.uid})
        if r.status_code == 200:
            return r.json()['word']
        elif r.status_code == 400:
            raise IndexError(r.json()['message'])
        else:
            raise RuntimeError("Unexpected exception:\nStatus code: %d\nResponse: %s" % (r.status_code, r.text()))

    # Call this to submit your answer
    def submit_answer(self, question_id, answer):
        r = requests.post(self.base_url + '/answer/%d' % question_id,\
                            data = {'answer': answer, 'id': self.uid})
        if r.status_code == 200:
            return r.json()['result']
        elif r.status_code == 400:
            raise ValueError(r.json()['message'])
        else:
            raise RuntimeError("Unexpected exception:\nStatus code: %d\nResponse: %s" % (r.status_code, r.text))

