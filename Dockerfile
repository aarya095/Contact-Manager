FROM python:3.13

WORKDIR /contacts-manager-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./alembic ./alembic
COPY ./app ./app
COPY ./config ./config

CMD [ "uvicorn", "app.main:app" ]