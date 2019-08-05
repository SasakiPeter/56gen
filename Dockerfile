FROM python:3.7.4

RUN apt-get update && apt-get install -y \
  sudo \
  python3-setuptools &&\
  apt-get clean && \ 
  rm -rf /var/lib/apt/lists/* &&\
  pip --no-cache-dir install \
  django \
  gunicorn \
  django-heroku \
  psycopg2 \ 
  pillow \ 
  boto3 \ 
  django-storages \ 
  django-markdownx