FROM ubuntu:22.04

WORKDIR /app
COPY . .

RUN apt update 
RUN apt install -y python3-pip python3-virtualenv sqlite3 libsqlite3-dev 
RUN virtualenv venv && . venv/bin/activate \
    && python3 -m pip install -r requirements.txt \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && python3 manage.py collectstatic --no-input

EXPOSE 8000

CMD . venv/bin/activate \
    && python3 manage.py runserver 0.0.0.0:8000