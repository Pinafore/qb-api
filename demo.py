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
        while next_q != -1:
            current_question = ""
            qlen = self._server.get_question_length(next_q)
            print("This question has %i tokens" % qlen)
            for ii in xrange(qlen):
                current_question += " %s" % self._server.get_word(next_q, ii)
                if any(x in current_question.lower() for x in self._patterns):
                    answer = [self._patterns[x] for x in self._patterns if
                              x in current_question][0]
                    print([x for x in self._patterns if
                           x in current_question][0])
                    print(next_q, current_question, answer)
                    self._server.submit_answer(next_q, answer)
                    break
            next_q = self._server.next_unanswered(self._user)

if __name__ == "__main__":
    user_id = 0
    server = QbApi(user_id)
    sa = StringAnswerer(server, user_id)
    sa.answer_questions()
