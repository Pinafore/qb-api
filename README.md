# qb-api

A server-side application to collect question answering data incrementally.  The basic overview of interactions are:
1. Get a user ID
2. Client connects to the server and gets a question ID
3. For each question, client requests as many words as it wants (by word id) and then submits an answer

Authentication and User IDs
====

Prereqs 
==== 

To run the software you must have the following python packages installed
* flask
* flask-restful
* requests

Running a Server
====

To start an instance of the server locally

```python api.py```

Currently this API has just two calls that can be made:

* /qb-api/question/\<questionId>/\<wordId>
    * POST
    * Request a word of a question
    * Required fields:
        * id: A valid user id (String)
    * Updates the number of words requested for this question to be wordId if it is not higher already already.
        * For example, if requests for words 0, 5, 1 and 1 of a particular question were sent, the user record of used words would be 0, 5, 5 and 5 respectively.

    * Returns: Word  #\<wordId> (indexed from 0) of question #\<questionId>
    * Example usage
    ```sh
        $ curl -X POST http://127.0.0.1:5000/qb-api/question/0/0 -d 'id=ident'
        {"word":"hello"}
    ```

* /qb-api/answer/\<questionId>
    * POST
    * Submit an answer for question #\<questionId>
    * Required fields: 
        * id: A valid user id (String)
        * answer: The answer for a question (String)
    * May only be called once per user per question
    * Example usage:
    ```sh
        $ curl -X POST http://127.0.0.1:5000/answer/0 -d 'id=0' -d 'answer=earth'
        {"score"=\<some score>}
    ```

* /qb-api/info/next/\<user_id>
 
Returns the next question ID that the user has yet to answer.

Note about answers: Answers must be the title of a wikipedia page. Answers are case sensitive.
