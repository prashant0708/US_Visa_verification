from us_visa.pipeline.prediction_pipeline import USVisaData,USVisaEstimator
from us_visa.logger import logging
from us_visa.entity.config_entity import ModelPusherConfig

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.constants import APP_HOST,APP_PORT

from fastapi import FastAPI , Request,Form
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
import uvicorn
from uvicorn import run as app_run
from typing import Annotated
import os
from glob import glob
import time
import pandas as pd

app = FastAPI()

## Load the model 
model_pusher_config = ModelPusherConfig()
Model_Bucket = model_pusher_config.Model_Pusher_Bucket_Name
Model_Path = model_pusher_config.S3_Key_Model_Pusher_Path


Model_estimator = USVisaEstimator(Bucket=Model_Bucket,model_path=Model_Path)


## pydantic model to prase valid input request

class USVisaRequest(BaseModel):
     continent:str
     education_of_employee:str
     has_job_experience:str
     requires_job_training:str
     no_of_employees:int
     region_of_employment:str
     prevailing_wage:float
     unit_of_wage:str
     full_time_position:str
     company_age:Annotated[int ,Field(..., gt=5,description = "Company age since it has establish")]


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict",response_class=HTMLResponse)
async def predict_us_visa(request: Request,
    continent: Annotated[str, Form()],
    education_of_employee: Annotated[str, Form()],
    has_job_experience: Annotated[str, Form()],
    requires_job_training: Annotated[str, Form()],
    no_of_employees: Annotated[int, Form()],
    region_of_employment: Annotated[str, Form()],
    prevailing_wage: Annotated[float, Form()],
    unit_of_wage: Annotated[str, Form()],
    full_time_position: Annotated[str, Form()],
    company_age: Annotated[int, Form(gt=5)]):
     try:
          visa_data = USVisaData(
               continent= continent,
               education_of_employee=education_of_employee,
               has_job_experience=has_job_experience,
               requires_job_training=requires_job_training,
               no_of_employees=no_of_employees,
               region_of_employment=region_of_employment,
               prevailing_wage=prevailing_wage,
               unit_of_wage=unit_of_wage,
               full_time_position=full_time_position,
               company_age=company_age
          )

          df = visa_data.get_usvisa_dataframe()
          logging.info(f"Data received from the user{df}")
          # Measure prediction time
          start_time = time.time()
          prediction = Model_estimator.predict(df)
          end_time = time.time()
          prediction_time = round(end_time - start_time, 4)  # in seconds
          logging.info(f"Prediction given and time taken {prediction_time} seconds")
          ## save the data for monitoring
          df["prediction"] = prediction
          df["prediction_time"] = prediction_time
          df.to_csv("prediction.csv", mode="a", header=not pd.io.common.file_exists("prediction.csv"), index=False)
          

          result = "Certified" if  prediction == 1.0 else "Denied"

          return templates.TemplateResponse("index.html", {"request": request, "result": result})
     except Exception as e:
        return {"error": str(e)}

@app.get("/train", response_class=HTMLResponse)
async def train_model(request: Request):
    try:
        logging.info("Training started")
        obj = TrainPipeline()
        obj.run_pipeline()
        logging.info("Training completed")
        # Immediately return the response while training runs in background
        return templates.TemplateResponse("index.html", {
            "request": request,
            "train_message": "Training Completed",
            "log_content": ""
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "train_message": "Training started in background...",
            "log_content": ""
        })
    
@app.get("/logs", response_class=HTMLResponse)
async def show_logs(request: Request):
    latest_log = ""
    if latest_log:
        with open(latest_log, "r") as file:
            log_content = file.read()
    else:
        log_content = "No logs found."

    return templates.TemplateResponse("index.html", {
        "request": request,
        "train_message": "",
        "log_content": log_content
    })
if __name__ == "__main__":
     uvicorn.run(app, host=APP_HOST, port=APP_PORT)
