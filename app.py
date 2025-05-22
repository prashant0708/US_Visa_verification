from us_visa.pipeline.prediction_pipeline import USVisaData,USVisaEstimator
from us_visa.entity.config_entity import ModelPusherConfig

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.constants import APP_HOST,APP_PORT

from fastapi import FastAPI , Request,Form,BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from uvicorn import run as app_run


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
     company_age:int


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict",response_class=HTMLResponse)
async def predict_us_visa(data:USVisaRequest):




     
     try:
          visa_data = USVisaData(
               continent= data.continent,
               education_of_employee=data.education_of_employee,
               has_job_experience=data.has_job_experience,
               requires_job_training=data.requires_job_training,
               no_of_employees=data.no_of_employees,
               region_of_employment=data.region_of_employment,
               prevailing_wage=data.prevailing_wage,
               unit_of_wage=data.unit_of_wage,
               full_time_position=data.full_time_position,
               company_age=data.company_age
          )

          df = visa_data.get_usvisa_dataframe()
          prediction = Model_estimator.predict(df)

          result = "Certified" if  prediction == 1.0 else "Denied"

          return {"prediction":result}
     except Exception as e:
        return {"error": str(e)}

@app.get("/train")
def train_model():
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        return {"message": "Training completed successfully"}
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
     uvicorn.run(app, host=APP_HOST, port=APP_PORT)
