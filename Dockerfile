# use official Python image
FROM python:3.12-slim

## set the working directory 

WORKDIR /app

## copy all source code

COPY . /app

## copy dependency list and install

RUN pip install --upgrade pip && pip install -r requirements.txt

#Start the FastAPI APP

CMD ["python3", "app.py"]

