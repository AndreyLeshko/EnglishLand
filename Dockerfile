FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt
CMD  ['python3 manage.py collectstatic --noinput', '&&', '/bin/sh','-c','python manage.py runserver']

COPY . /app/