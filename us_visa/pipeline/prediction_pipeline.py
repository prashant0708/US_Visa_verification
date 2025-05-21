from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION

from us_visa.entity.config_entity import USvisaPredictorConfig
from pandas import DataFrame
import pandas as pd
from us_visa.entity.s3_estimator import USVisaEstimator
import sys

class USVisaData:
    def __init__(self,continent,
                education_of_employee,
                has_job_experience,
                requires_job_training,
                no_of_employees,
                region_of_employment,
                prevailing_wage,
                unit_of_wage,
                full_time_position,
                company_age):
        """   
        Input feature to predict 
        """
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age
        except Exception as e:
            raise USVISAEXCEPTION(e,sys)
        
    def get_us_data_dict(self):
        try:
            inputs = {
                "continent":[self.continent],
                "education_of_employee":[self.education_of_employee],
                "has_job_experience":[self.has_job_experience],
                "requires_job_training":[self.requires_job_training],
                "no_of_employees":[self.no_of_employees],
                "region_of_employment":[self.region_of_employment],
                "prevailing_wage":[self.prevailing_wage],
                "unit_of_wage":[self.unit_of_wage],
                "full_time_position":[self.full_time_position],
                "company_age":[self.company_age]
            }
            return inputs
        except Exception as e:
            raise USVISAEXCEPTION(e,sys)
    def get_usvisa_dataframe(self)->DataFrame:
        try:
            usvisa_dict = self.get_us_data_dict()
            return pd.DataFrame(usvisa_dict)
        except Exception as e:
            raise USVISAEXCEPTION(e,sys)
        
class usvisaclassifier:
    def __init__(self, prediction_pipeline_config:USvisaPredictorConfig =USvisaPredictorConfig()):
        try:
            self.prediction_pipeline_config=prediction_pipeline_config
        except Exception as e:
            raise USVISAEXCEPTION(e,sys)
        
    def predict(self,dataframe):
        try:
            logging.info("Loading the model from the s3 bucket")

            model = USVisaEstimator(Bucket=self.prediction_pipeline_config.model_bucket_name,
                                    model_path=self.prediction_pipeline_config.model_file_path)
            logging.info(f"Model loaded from s3 bucket{model}")
            
            result = model.predict(DataFrame)
            logging.info(f"Prediction result from the model{result}")
            return result
        

        except Exception as e:
            raise USVISAEXCEPTION(e,sys)
