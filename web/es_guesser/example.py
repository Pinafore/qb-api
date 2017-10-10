import os
import sys
import time
import numpy as np
from retrying import retry
from guesser import ElasticSearchGuesser
from datasets import QuizBowlDataset
sys.path.append('../')
from client import QbApi

user_id = os.environ.get('QB_USER_ID', 1)
api_key = os.environ.get('QB_API_KEY', 'key')
qb_host = os.environ.get("QB_HOST", 'http://qb.entilzha.io')
QB_QUESTION_DB = 'non_naqt.db'

base_url = qb_host + '/qb-api/v1'
server = QbApi(base_url, user_id, api_key)


class ThresholdBuzzer:

    def __init__(self, threshold=0.3):
        self.threshold = threshold

    def normalize(self, scores):
        s = sum(scores)
        scores = [x / s for x in scores]
        return scores

    def buzz(self, guesses, position):
        '''Given a sorted list of guesses and their scores, 
        decide buzzing or not.
        '''
        guesses = sorted(guesses, key=lambda x: x[1])[::-1]
        scores = self.normalize([x[1] for x in guesses])
        buzz = (scores[0] > self.threshold) and (position > 40)
        return buzz


@retry(wait_fixed=60000, 
       stop_max_attempt_number=10)
def submit_answer(qid, answer):
    time.sleep(1) # delay one second
    server.submit_answer(qid, answer)

@retry(wait_fixed=60000, 
       stop_max_attempt_number=10)
def get_word(qid, i):
    time.sleep(1) # delay one second
    return server.get_word(qid, i)

def main():
    # train elasticsearch guesser
    esguesser = ElasticSearchGuesser()
    qb_dataset = QuizBowlDataset(
            min_class_examples=1, 
            guesser_train=True,
            qb_question_db=QB_QUESTION_DB)
    training_data = qb_dataset.training_data()
    esguesser.train(training_data, rebuild_index=False)

    # setup threshold based buzzer
    buzzer = ThresholdBuzzer()

    # answer questions
    all_questions = server.get_all_questions()
    print(str(all_questions)[:70] + "...")

    for qdict in [x for x in all_questions]:
        next_q = int(qdict['id'])
        qlen = int(qdict['word_count'])
        print("\n\nAnswering question %i, which has %i tokens" % (next_q, qlen))

        current_question = ''
        answer = ''
        for i in range(qlen):
            curr_word_info = get_word(next_q, i)
            curr_word = curr_word_info['text']
            print(curr_word, end=' ')
            current_question += ' ' + curr_word
            
            guesses = esguesser.guess(current_question)
            guesses = sorted(guesses, key=lambda x: x[1])[::-1]
            answer = guesses[0][0]

            if(buzzer.buzz(guesses, i)):
                print("\nANSWERING! %i %i (%s, %f sec)" %
                      (next_q, i, answer))
                submit_answer(next_q, answer)
                break
            sys.stdout.flush()

        # Submit some answer if the question is unanswered by the end
        if answer == '':
            answer = "Chinua Achebe"
        print("\nANSWERING! %i %i (%s)" %
                (next_q, qlen, answer))
        submit_answer(next_q, answer)

if __name__ == '__main__':
    main()

