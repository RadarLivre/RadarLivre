FROM ubuntu:22.04

WORKDIR /app
COPY . .

RUN apt update \
  && apt install -y python3-pip \
  && apt clean

RUN python3 -m pip install -r requirements.txt

#RUN python3 manage.py migrate
#RUN python3 manage.py collectstatic --no-input

RUN chmod +x runserver.sh

EXPOSE 8000