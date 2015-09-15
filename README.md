# qb-api

Currently this API has just two calls that can be made:

* /qb-api/question//<questionId>//<wordId>
    * POST
    * Request a word of a question
    * Required fields:
        * id: A valid user id (String)
    * Updates the number of words requested for this question to be wordId if it is not higher already already.
        * For example, if requests for words 0, 5, 1 and 1 of a particular question were sent, the user record of used words would be 0, 5, 5 and 5 respectively.

    * Returns: Word  #/<wordId> (indexed from 0) of question #/<questionId>
    * Example usage
    ```sh
        $ curl -X POST http://127.0.0.1:5000/qb-api/question/0/0 -d 'id=ident'
        {"word":"hello"}
    ```

* /qb-api/answer//<questionId>
    * POST
    * Submit an answer for question #/<questionId>
    * Required fields: 
        * id: A valid user id (String)
        * answer: The answer for a question (String)
    * May only be called once per user per question
    * Example usage:
    ```sh
        $ curl -X POST http://127.0.0.1:5000/answer/0 -d 'id=0' -d 'answer=earth'
        {"score"=/<some score>}
    ```

Note about answers: Answers must be the title of a wikipedia page. Answers are case insensitive.
