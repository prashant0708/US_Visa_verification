# use official Python image
FROM python:3.12-slim

## set the working directory 

WORKDIR /app

## copy all source code

COPY . /app

## copy dependency list and install

RUN pip install --upgrade pip && pip install -r requirements.txt

## create .project-root file to fix from_root detection 
RUN touch /app/.project-root

#Start the FastAPI APP

CMD ["python3", "app.py"]

