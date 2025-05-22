from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import sys
import posixpath
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

from us_visa.pipeline.training_pipeline import TrainPipeline

from us_visa.entity.config_entity import DataIngestionConfig 
from us_visa.configuration.aws_config import S3Client
from us_visa.pipeline.prediction_pipeline import USVisaData,usvisaclassifier
from us_visa.constants import *
import dill

import io

from us_visa.entity.s3_estimator import USVisaEstimator

from us_visa.configuration.aws_config import S3Client

S3_Client=S3Client()


obj = TrainPipeline()
obj.run_pipeline()

# OBJ = USVisaData(continent="Asia",education_of_employee="High School",
#                  has_job_experience="Y",requires_job_training="N",no_of_employees=800,
#                  region_of_employment="Northeast",prevailing_wage=100000,unit_of_wage="Year",full_time_position='Y',
#                  company_age=10)
# df = OBJ.get_usvisa_dataframe()

# model_pusher_config = ModelPusherConfig()
# Model_Bucket = model_pusher_config.Model_Pusher_Bucket_Name
# Model_Path = model_pusher_config.S3_Key_Model_Pusher_Path

# def load_model(bucket,path): 
#         response = S3_Client.s3_client.get_object(Bucket=bucket,Key=path)
#         model_binary = response['Body'].read()
#         model = dill.load(io.BytesIO(model_binary))
#         return model

# model = load_model(bucket=Model_Bucket,path =Model_Path)

# result = model.predict(df)
# if result == 1.:
#     print("Certified")
# else:
#       print("Denied")

# estimator = USVisaEstimator(Bucket=Model_Bucket,model_path=Model_Path)


# predict = estimator.predict(dataframe=df)

# if predict == 1.:
#     print("Certified")
# else:
#       print("Denied")


