FROM python:3.11.3-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install build-essential -y

RUN pip install --upgrade pip Cython
RUN pip install pipenv
RUN pipenv sync --system

ARG PORT=8000
ENV PORT=$PORT
EXPOSE $PORT

CMD python main.py
