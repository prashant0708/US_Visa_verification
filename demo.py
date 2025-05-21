from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys
import posixpath

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from us_visa.configuration.aws_config import S3Client
from us_visa.pipeline.prediction_pipeline import USVisaData,usvisaclassifier
from us_visa.constants import *
import dill
from us_visa.constants import *
from us_visa.configuration.aws_config import S3Client
import io
S3_Client=S3Client()

OBJ = USVisaData(continent="Europe",education_of_employee="Master's",
                 has_job_experience="Y",requires_job_training="N",no_of_employees=1637,
                 region_of_employment="Midwest",prevailing_wage=154170.99,unit_of_wage="Year",full_time_position='Y',
                 company_age=20)
df = OBJ.get_usvisa_dataframe()

MODEL_BUCKET_NAME = "us-visa-artifact"
MODEL_FILE_NAME = "artifact/US_VISA/2025-05-21-16-22-38/model_trainer/model.pkl"

def load_model(bucket,path): 
        response = S3_Client.s3_client.get_object(Bucket=bucket,Key=path)
        model_binary = response['Body'].read()
        model = dill.load(io.BytesIO(model_binary))
        return model

model = load_model(bucket=MODEL_BUCKET_NAME,path =MODEL_FILE_NAME)

result = model.predict(df)
if result == 1.:
    print("Certified")
else:
      print("Denied")




