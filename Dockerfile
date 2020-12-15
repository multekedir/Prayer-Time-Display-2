FROM python:3.8
RUN pip install pipenv

WORKDIR /app
COPY . /app
COPY Pipfile* /tmp/

RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ENV FLASK_APP app.py

EXPOSE 5000

ENTRYPOINT ["./run.sh"]
