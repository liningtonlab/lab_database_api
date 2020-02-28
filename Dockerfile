# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7-slim-buster

# If you prefer miniconda:
# FROM continuumio/miniconda3

LABEL Name=liningtondb-api Version=0.1
WORKDIR /app
COPY ./requirements.txt /app
COPY ./jwt.key /app
COPY ./jwt.key.pub /app
# Using pip:
# RUN python3 -m pip install -r requirements.txt
# CMD ["python3", "-m", "curator_v3"]

# Using pipenv:
# RUN python3 -m pip install pipenv
# RUN pipenv install --ignore-pipfile
# CMD ["pipenv", "run", "python3", "-m", "curator_v3"]

# Using miniconda (make sure to replace conda'myenv' w/ your environment name):
# RUN conda create -n myenv python=3


# Still run requirements install but should be fast if all installed
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

RUN python3 -m pip install gunicorn gevent
RUN useradd -ms /bin/bash gunicorn

ENV SECRET_KEY="TOPSECRET"
ENV DATABASE_URL="mysql+pymysql://jvansan:jvansan@mysql/linington_lab"
ENV BASE_URL="localhost"
ENV UPLOAD_DIR="/app/uploads"
COPY ./run-server.sh /app

ADD ./api /app/api
CMD /bin/bash run-server.sh
