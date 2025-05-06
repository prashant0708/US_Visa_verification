import os 
from datetime import datetime
from datetime import date


ROOT_DIR = os.getcwd()
CURRENT_TIME_STEMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "Visa_Data"

PIPELINE_NAME = "US_VISA"


ARTIFACT_DIR_NAME = "artifact"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")

""" 
Data Ingestion related constant start with Data_Ingestion VAR NAME 
"""
DATA_INGESTION_DIR_NAME = "data_ingestion"
RAW_FILE_DIR = "RAW_FILE"
RAW_DATA = "US_VISA.csv"
SPLITED_FILE_DIR ="SPLITED"
TRAIN_DATA = "Train.csv"
TEST_DATA = "Test.csv"
TEST_SIZE = 0.2

""" 
Data Validation related constant start with Data_Validation VAR NAME 
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME :str  = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str = "report.yaml"

"""  
Data Transformation related constant start with Data Transformation 
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR :str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object" 
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME:str = "Train.npy"
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME:str = "TEST.npy"



"""  
Model training related constant start with Model Training
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_NAME :str = "trained_Model"
MODEL_TRAINER_TRAINER_MODEL_NAME:str = "model.pkl" 
MODEL_TRAINER_EXPECTED_ACCURACY:float = 0.6
MODEL_TRAINER_MODEL_CONFIG_PATH:str = os.path.join('config','model.yaml')







