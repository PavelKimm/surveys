FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

COPY requirements.txt $APP_HOME/requirements.txt
WORKDIR $APP_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
