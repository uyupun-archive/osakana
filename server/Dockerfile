FROM python:3.11.3-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --sync

ARG PORT=8000
ENV PORT=$PORT
EXPOSE $PORT

CMD python main.py
