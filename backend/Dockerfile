FROM python:3.8.5

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/scr/requirements.txt
RUN pip install -r /usr/scr/requirements.txt

COPY . .
EXPOSE 8000