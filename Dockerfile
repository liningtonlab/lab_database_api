FROM python:3.8-slim-buster

LABEL Name=liningtondb-api Version=0.1
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*
RUN ssh-keygen -t rsa -b 4096 -m PEM -f jwt.key -N '' \
    && openssl rsa -in jwt.key -pubout -outform PEM -out jwt.key.pub

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
