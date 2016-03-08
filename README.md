# Quiz Bowl API

Using the code in this repository you can:

1. Query our Quiz Bowl API server run at [qb.boydgraber.org](qb.boydgraber.org)
2. Run your on Quiz Bowl API server

## Query Quiz Bowl API Server
The main objective of querying the Quiz Bowl API is to evaluate the performance of your system. This requires you to connect to the evaluation server, get a question word by word, and return an answer.  To do so, you must follow these steps to install the required software, acquire and API key, and test your system.

### Create an Account and API Key
Visit [http://qb.boydgraber.org/register](qb.boydgraber.org/register). The page will redirect you to Google for OAuth authentication. We only require a valid email. The page will then redirect you to a page that contains a json response with your email, user id, and API key. Be sure to save this information, but if you lose it you can visit the register link again and the website will redisplay your credentials.

You should get something that looks like:
```
{
"api_key": "secret-here",
"email": "jvaljean@gmail.com",
"id": 24601
}
```

### Required Software
The QB API uses JSON for all communication which means it interops with any user language. However, we have included a python client implementation along with a demonstration of querying the server in `web/client.py` and `web/demo.py` respectively. Required software is:

1. Python 3
2. `requests` package installable via `pip install requests`

### Configuration
Set the following environment variables in your `.bashrc` or equivalent to run `web/demo.py`:

```bash
export QB_USER_ID=1
export QB_API_KEY='secret-here'
```

The demo answerer goes through all the questions and answers based on fixed strings (this is pretty dumb, but hopefully gives an idea of how to write your own answerer!).  For example, whenever it sees "author" it answers "Marcel Proust", whenever it sees "fancy" it answers "Iggy Azalea", and its default answer at the end of a question is "Chinua Achebe".

It first gets all of the questions it can answer from the `web/client.py` API:
```
all_questions = self._server.get_all_questions()
print(str(all_questions)[:70] + "...")
for qdict in all_questions:
     start = time.time()
     next_q = int(qdict['id'])
     qlen = int(qdict['word_count'])
```
which returns a list of dictionaries (each dictionary is a question JSON):
```
[{'word_count': 90, 'id': 1}, {'word_count': 87, 'id': 2}, {'word_count': 96, 'id': 3}, {'word_count': 81, 'id': 4}, {'word_count': 90, 'id': 5}, {'word_count': 88, 'id': 6}, {'word_count': 88, 'id': 7}, {'word_count': 84, 'id': 8}, {'word_count': 98, 'id': 9}, {'word_count': 92, 'id': 10}, {'word_count': 88, 'id': 11}, {'word_count': 100, 'id': 12}, {'word_count': 82, 'id': 13}, {'word_count': 97, 'id': 14}, {'word_count': 92, 'id': 15}, {'word_count': 101, 'id': 16}, {'word_count': 99, 'id': 17}, {'word_count': 103, 'id': 18}, {'word_count': 93, 'id': 19}, {'word_count': 96, 'id': 20}, {'word_count': 97, 'id': 21}, {'word_count': 91, 'id': 22}, {'word_count': 80, 'id': 23}, {'word_count': 93, 'id': 24}, {'word_count': 89, 'id': 25}, {'word_count': 89, 'id': 26}, {'word_count': 106, 'id': 27}, {'word_count': 94, 'id': 28}, {'word_count': 102, 'id': 29}, {'word_count': 100, 'id': 30}, {'word_count': 100, 'id': 31}, {'word_count': 95, 'id': 32}, {'word_count': 101, 'id': 33}, {'word_count': 97, 'id': 34}, {'word_count': 96, 'id': 35}, {'word_count': 93, 'id': 36}, {'word_count': 95, 'id': 37}, {'word_count': 98, 'id': 38}, {'word_count': 97, 'id': 39}, {'word_count': 86, 'id': 40}, {'word_count': 88, 'id': 41}, {'word_count': 98, 'id': 42}, {'word_count': 96, 'id': 43}, {'word_count': 91, 'id': 44}, {'word_count': 90, 'id': 45}]
```

It then iterates over the questions one word at a time:
```
self._server.get_question_length(next_q)
     for ii in range(qlen):
          ....
```

### JSON Documentation
The Quiz Bowl API is documented via a [Swagger JSON spec](http://swagger.io/). You can view a very nice version of the documentation via the [Swagger UI Website](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/Pinafore/qb-api/master/swagger.json) (Note: the "try it now" feature doesn't work due to XSS attack protection). Alternatively you can load a "light" version of the docs by opening `docs/index.html` in a web browser. The specification files are in `swagger.yaml` and `swagger.json`. Finally, you can generate a client in one of many languages by:

1. Navigating to [editor.swagger.io](http://editor.swagger.io/#/)
2. Uploading the specification file by clicking "file" then "import file" then "Generate Client" and choose your language

### Raw CURL Commands

The Swagger documentation (above) can be used to generate CURL commands (or other frameworks).  For example, you can get the raw JSON of all questions to answer using:
```
curl -X GET --header 'Accept: application/json' 'http:/qb.boydgraber.org/qb-api/v1/questions?api_key=secret-here'
```

## Run Quiz Bowl API Server
To run a standalone instance of the Quiz Bowl API server is very easy using [Docker](https://www.docker.com/). First, you will need to install [Docker Engine](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/). After doing so and starting a Docker Machine, run the following commands to launch the server:

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

This will run the server in blocking mode, you can run it in the background with `docker-compose up -d`. To test that it works you can run
```bash
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up
```

You should see `demo.py` running and answering questions. Note, that this will leave the database in a "dirty" state. You can bring the database to a clean state by having the server running, then running:

```bash
docker exec -it qbapi_web_1 bash
python
```

Then in the python session

```python
>>> import app
>>> import database
>>> app.db.drop_all()
>>> app.db.create_all()
>>> database.load_questions()
```

### Configuration
The instructions that follow are for running an instance with oauth. The documentation may not be complete

* A `client_secrets.json` file must be created with the following contents:
```json
"web": {
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "redirect_uris": ["<domain>/oauth2callback"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```
  * `client_id` and `client_secret` should be obtained from the Google developer's console for your account.
  * domain example: http://mydomain.com/

* A config.py file should be present with the single line:
```python
SECRET_KEY='mysecretkey'
```
