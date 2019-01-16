# Quiz Bowl API

This repository is deprecated, please visit qanta.org to participate in Quizbowl

Using the code in this repository you can:

1. Query our Quiz Bowl API server run at (No longer running)
2. Run your on Quiz Bowl API server

## Query Quiz Bowl API Server
The main objective of querying the Quiz Bowl API is to evaluate the performance of your system. This requires you to connect to the evaluation server, get a question word by word, and return an answer.  To do so, you must follow these steps to install the required software, acquire and API key, and test your system.

### Create an Account and API Key
Visit [/register](/register). The page will redirect you to Google for OAuth authentication. We only require a valid email. The page will then redirect you to a page that contains a json response with your email, user id, and API key. Be sure to save this information, but if you lose it you can visit the register link again and the website will redisplay your credentials.

You should get something that looks like:
```
{
"api_key": "secret-here",
"email": "jvaljean@gmail.com",
"id": 24601
}
```

### Note on Answers

All answers correspond to exactly one wikipedia page with whitespaces replaced with underscores. Note that this means that things such as accented characters may be part of answers since Wikipedia page titles contain these. To mitigate the possibility of answers that are barely incorrect due to trivial mistakes we are providing a file containing all possible wikipedia pages as they appear in the answer set. Since this changed was implemented relatively late (10/9) during the upload of the test data we will consider an answer correct if it satisfies one of the following conditions supposing `s_answer` is the submitted answer and `t_answer` is the true answer. Unidecode can be found here https://pypi.python.org/pypi/Unidecode, and is a package that converts non-ascii characters to their closest visual equivalent.

* `s_answer == t_answer`
* `unidecode(s_answer) == unidecode(t_answer)`
* `s_answer.lower() == t_answer.lower()`
* `unidecode(s_answer).lower() == unidecode(t_answer).lower()`

Wikipedia Pages:

* Line separated text: https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/preprocess/wikipedia-titles.txt
* Python pickle file returning set of string pages (python 3.6): https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/preprocess/wikipedia-titles.pickle 

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
for qdict in [x for x in all_questions if x['fold'] == 'dev']:
     start = time.time()
     next_q = int(qdict['id'])
     qlen = int(qdict['word_count'])
```
which returns a list of dictionaries (each dictionary is a question JSON):
```
[{'word_count': 90, 'id': 1, 'fold': 'dev'}, {'word_count': 87, 'id': 2, 'fold': 'dev'}, {'word_count': 96, 'id': 3, 'fold': 'dev'}, {'word_count': 81, 'id': 4, 'fold': 'dev'}, {'word_count': 90, 'id': 5, 'fold': 'dev'}, {'word_count': 88, 'id': 6, 'fold': 'dev'}, {'word_count': 88, 'id': 7, 'fold': 'dev'}, {'word_count': 84, 'id': 8, 'fold': 'dev'}, {'word_count': 98, 'id': 9, 'fold': 'dev'}, {'word_count': 92, 'id': 10, 'fold': 'dev'}, {'word_count': 88, 'id': 11, 'fold': 'dev'}, {'word_count': 100, 'id': 12, 'fold': 'dev'}, {'word_count': 82, 'id': 13, 'fold': 'dev'}, {'word_count': 97, 'id': 14, 'fold': 'dev'}, {'word_count': 92, 'id': 15, 'fold': 'dev'}, {'word_count': 101, 'id': 16, 'fold': 'dev'}, {'word_count': 99, 'id': 17, 'fold': 'dev'}, {'word_count': 103, 'id': 18, 'fold': 'dev'}, {'word_count': 93, 'id': 19, 'fold': 'dev'}, {'word_count': 96, 'id': 20, 'fold': 'dev'}, {'word_count': 97, 'id': 21, 'fold': 'dev'}, {'word_count': 91, 'id': 22, 'fold': 'dev'}, {'word_count': 80, 'id': 23, 'fold': 'dev'}, {'word_count': 93, 'id': 24, 'fold': 'dev'}, {'word_count': 89, 'id': 25, 'fold': 'dev'}, {'word_count': 89, 'id': 26, 'fold': 'dev'}, {'word_count': 106, 'id': 27, 'fold': 'dev'}, {'word_count': 94, 'id': 28, 'fold': 'dev'}, {'word_count': 102, 'id': 29, 'fold': 'dev'}, {'word_count': 100, 'id': 30, 'fold': 'dev'}, {'word_count': 100, 'id': 31, 'fold': 'dev'}, {'word_count': 95, 'id': 32, 'fold': 'dev'}, {'word_count': 101, 'id': 33, 'fold': 'dev'}, {'word_count': 97, 'id': 34, 'fold': 'dev'}, {'word_count': 96, 'id': 35, 'fold': 'dev'}, {'word_count': 93, 'id': 36, 'fold': 'dev'}, {'word_count': 95, 'id': 37, 'fold': 'dev'}, {'word_count': 98, 'id': 38, 'fold': 'dev'}, {'word_count': 97, 'id': 39, 'fold': 'dev'}, {'word_count': 86, 'id': 40, 'fold': 'dev'}, {'word_count': 88, 'id': 41, 'fold': 'dev'}, {'word_count': 98, 'id': 42, 'fold': 'dev'}, {'word_count': 96, 'id': 43, 'fold': 'dev'}, {'word_count': 91, 'id': 44, 'fold': 'dev'}, {'word_count': 90, 'id': 45, 'fold': 'dev'}]
```

It then iterates over the questions one word at a time:
```
self._server.get_question_length(next_q)
     for ii in range(qlen):
          ....
```

### Folds

*IMPORTANT*: The sample code provided answers all available 'dev' questions.  You can answer 'dev' questions as many times as you like.  However, 'test' questions can only be answered once.  So be very careful when querying the text of test questions and providing your answers.

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

## Example System Using the API

We provide an example system in `web/es_guesser` that is composed of
[ElasticSearch](https://www.elastic.co/products/elasticsearch) as guesser, and
a very simple threshold based buzzer. This system built on a simplified
version of [Qanta](https://github.com/Pinafore/qb).

### Dependencies
First, install and run ElasticSearch:

```
$ curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.2.tar.gz
$ tar -xvf elasticsearch-5.2.2.tar.gz
$ cd elasticsearch-5.2.2
$ bash bin/elasticsearch
```

ElasticSearch runs at `localhost:9200`.

Then install ElasticSearch python packages: `elasticsearch` and
`elasticsearch-dsl`.

```
$ pip install elasticsearch elasticsearch-dsl
```

### Data
The example code uses `web/es_guesser/non_naqt.db` which can be found
[here](https://github.com/Pinafore/qb/blob/master/data/internal/non_naqt.db).

### Running the System
To run the system, simply go to `web/es_guesser` and run `python example.py`.
It will train the guesser and answer questions using the API.

Unlike neural network systems where the parameters need to be stored after
training and loaded when testing, ElasticSearch doesn't require saving and
loading the parameters. The data and other information are stored in index
files and will be persistent even after ElasticSearch is stopped, so you don't
need to re-train or load any parameters after restarting it.
