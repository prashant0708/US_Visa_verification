import os 
from datetime import datetime


ROOT_DIR = os.getcwd()
CURRENT_TIME_STEMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "Visa_Data"

PIPELINE_NAME = "US_VISA"


ARTIFACT_DIR_NAME = "artifact"

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







