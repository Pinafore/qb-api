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
        next_q = self._server.next(
        while

if __name__ == "__main__":
