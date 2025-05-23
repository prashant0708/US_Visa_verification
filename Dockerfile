# use official Python image
FROM python:3.12.7

## set the working directory 

WORKDIR /app

## copy dependency list and install

copy requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

## copy all source code

COPY . .

## Expose the fastapi port

EXPOSE 8080

#Start the FastAPI APP

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

