FROM ubuntu

WORKDIR /app
COPY . .

RUN apt update 
RUN apt install -y python3-pip python3-virtualenv sqlite3 libsqlite3-dev 
# RUN virtualenv venv 
# RUN source venv/bin/activate 
RUN python3 -m pip install -r requirements.txt 
RUN python3 manage.py makemigrations 
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000