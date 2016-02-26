import unittest
import requests


class QuizBowlTests(unittest.TestCase):
    def test_status(self):
        response = requests.get('http://127.0.0.1:5000/status')
        print(response.text)
        body = response.json()
        self.assertEqual(body['status'], 'OK')
