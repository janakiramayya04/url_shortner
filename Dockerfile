FROM python:3.16.6-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn app.main.app 