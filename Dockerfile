FROM python:3

RUN mkdir -p /usr/src/app
ADD requirements.txt /usr/src/app/
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ADD . /usr/src/app

EXPOSE 5000

CMD ["python", "api.py"]
