from client import QbApi


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
        for qdict in self._server.get_all_questions():
            next_q = int(qdict['id'])
            qlen = int(qdict['word_count'])
            current_question = ""
            qlen = self._server.get_question_length(next_q)
            print("Currently answering question %i, which has %i tokens" % \
                (next_q, qlen))
            for ii in range(qlen):
                current_question += " %s" % self._server.get_word(next_q, ii)
                print(current_question)
                if answer == "" and any(x in current_question.lower()
                                        for x in self._patterns):
                    answer = [self._patterns[x] for x in self._patterns if
                              x in current_question.lower()][0]
                    print("ANSWERING! %i %i (%s)" % (next_q, ii, answer))
                    print(next_q, current_question, answer)
                    self._server.submit_answer(next_q, answer)

            # If we haven't answered anything by the end of the question, hard
            # to go wrong with this answer
            if answer == "":
                self._server.submit_answer(next_q, "Chinua Achebe")

            answer = ""

if __name__ == "__main__":

    # mohit's credentials (for debugging)
    user_id = 7
    base_url = 'http://qb.boydgraber.org/qb-api/v1'
    api_key = 'lIqlnLuNfoLZqNbgwYNSmTfRFoxqVeBYzgrMsBwFmdXEhZMRPivXefJiqVNtxGiH'
    server = QbApi(base_url, user_id, api_key)
    sa = StringAnswerer(server)
    sa.answer_questions()
