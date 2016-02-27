from client import QbApi
import unittest


class QuizBowlClientTests(unittest.TestCase):
    def test_get_num_questions(self):
        client = QbApi(0)
        num_qs = client.get_num_questions()
        self.assertIsInstance(num_qs, int)
        self.assertTrue(num_qs > 0)

    def test_get_question_length(self):
        client = QbApi(0)
        q_length = client.get_question_length(0)
        self.assertIsInstance(q_length, int)
        self.assertTrue(q_length > 0)

    def test_get_word(self):
        client = QbApi(0)
        word = client.get_word(0, 0)
        self.assertIsInstance(w, str)
        self.assertTrue(w)

    def test_submit_answer_success(self):
        client = QbApi(0)
        res = client.submit_answer(0, 'abcasdfasdfasdf')
        self.assertEqual(res, False)

    def test_submit_answer_duplicate(self):
        client = QbApi(0)
        client.submit_answer(0, 'answer1')
        self.assertRaises(ValueError, client.submit_answer(0, 'answer2'))
