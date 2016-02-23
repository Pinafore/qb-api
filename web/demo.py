from client import QbApi


class StringAnswerer:
    """
    A really dumb system to answer questions based on string matches
    """

    def __init__(self, server, user, patterns={"watergate": "Richard Nixon",
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
        self._user = user

    def answer_questions(self):
        """
        Answer questions

        """
        next_q = self._server.next_unanswered(self._user)
        answer = ""
        while next_q != -1:
            current_question = ""
            qlen = self._server.get_question_length(next_q)
            print("This question has %i tokens" % qlen)
            for ii in range(qlen):
                current_question += " %s" % self._server.get_word(next_q, ii)
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

            next_q = self._server.next_unanswered(self._user)
            print("Moving on to question %i" % next_q)
            answer = ""

if __name__ == "__main__":
    user_id = 0
    server = QbApi(user_id)
    sa = StringAnswerer(server, user_id)
    sa.answer_questions()
