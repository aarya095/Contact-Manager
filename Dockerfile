FROM python:3.13

WORKDIR /contacts-manager-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app" "--reload"]