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

It first gets all of the questions it can answer from the `web/client.py` API.  

```
all_questions = self._server.get_all_questions()
print(str(all_questions)[:70] + "...")
for qdict in all_questions:
     start = time.time()
     next_q = int(qdict['id'])
     qlen = int(qdict['word_count'])
```



### JSON Documentation
The Quiz Bowl API is documented via a [Swagger JSON spec](http://swagger.io/). You can find the specification files in `swagger.yaml` and `swagger.json`. This allows you to browse our API documentation online by loading `docs/index.html` in your browser. You can also visit [the swagger ui demo](http://petstore.swagger.io/) and replace the url with `https://raw.githubusercontent.com/Pinafore/qb-api/master/swagger.json`. Finally, you can generate a client in one of many languages by:

1. Navigating to [editor.swagger.io](http://editor.swagger.io/#/)
2. Uploading the specification file by clicking "file" then "import file" then "Generate Client" and choose your language

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
