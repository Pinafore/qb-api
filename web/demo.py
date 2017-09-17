from client import QbApi
import sys, time
import os

user_id = os.environ.get('QB_USER_ID', 1)
api_key = os.environ.get('QB_API_KEY', 'key')
qb_host = os.environ.get("QB_HOST", 'http://qb.entilzha.io')


class StringAnswerer:
    """
    A really dumb system to answer questions based on string matches
    """

    def __init__(self, server, patterns={"watergate": "Richard Nixon",
                                         "republican": "Donald Trump",
                                         "people": "Maori people",
                                         "found": "Sri Lanka",
                                         "this man": "Erwin Rommel",
                                         "author": "Marcel Proust",
                                         "organ": "Spleen",
                                         "opera": "Porgy and Bess",
                                         "fancy": "Iggy Azalea"}):
        self._server = server
        self._patterns = patterns
        self._buffer = []

    def answer_questions(self):
        """
        Answer questions

        """

        answer = ""
        all_questions = self._server.get_all_questions()
        print(str(all_questions)[:70] + "...")
        for qdict in [x for x in all_questions if x['fold'] == 'test']:
            start = time.time()
            next_q = int(qdict['id'])
            qlen = int(qdict['word_count'])
            current_question = ""
            qlen = self._server.get_question_length(next_q)
            print("Answering question %i, which has %i tokens" %
                  (next_q, qlen))
            for ii in range(qlen):
                curr_word_info = self._server.get_word(next_q, ii)
                curr_word = curr_word_info['text']
                print(curr_word, end=' ')
                current_question += ' ' + curr_word
                if answer == "" and any(x in current_question.lower()
                                        for x in self._patterns):
                    answer = [self._patterns[x] for x in self._patterns if
                              x in current_question.lower()][0]
                    print("\nANSWERING! %i %i (%s, %f sec)" %
                          (next_q, ii, answer, time.time() - start))
                    self._server.submit_answer(next_q, answer)
                    break
                sys.stdout.flush()

            # Submit some answer if the question is unanswered by the end
            if answer == "":
                print("\nANSWERING! %i %i (%s)" %
                      (next_q, qlen, "Chinua Achebe"))
                self._server.submit_answer(next_q, "Chinua Achebe")

            answer = ""
            print("took %f seconds\n" % (time.time() - start, ))

if __name__ == "__main__":

    base_url = qb_host + '/qb-api/v1'
    server = QbApi(base_url, user_id, api_key)
    sa = StringAnswerer(server)
    sa.answer_questions()
