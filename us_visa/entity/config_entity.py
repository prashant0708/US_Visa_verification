from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION



class TrainingPipeLineConfig:
    root_dir = ROOT_DIR
    pipeline_name = PIPELINE_NAME
    Current_time_stemp = CURRENT_TIME_STEMP
    artifact_dir = os.path.join(root_dir,ARTIFACT_DIR_NAME,pipeline_name,Current_time_stemp)
    
    


training_pipeline_config : TrainingPipeLineConfig=TrainingPipeLineConfig()


class DataIngestionConfig:
    data_ingestion_dir_path = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    raw_file_dir_path = os.path.join(data_ingestion_dir_path,RAW_FILE_DIR)
    raw_data_file_path = os.path.join(raw_file_dir_path,RAW_DATA)
    splited_file_dir_path = os.path.join(data_ingestion_dir_path,SPLITED_FILE_DIR)
    training_file_path = os.path.join(splited_file_dir_path,TRAIN_DATA)
    testing_file_path = os.path.join(splited_file_dir_path,TEST_DATA)

class DataValidationConfig:
    data_validation_dir_path = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
    data_validation_drift_report_dir_name = os.path.join(data_validation_dir_path,DATA_VALIDATION_DRIFT_REPORT_DIR_NAME,CURRENT_TIME_STEMP)
    data_validation_drift_report_file_path = os.path.join(data_validation_drift_report_dir_name,DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    data_transformation_dir_path = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    data_transformation_transformed_data_dir = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
    data_transformation_transformed_object_dir = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)
    
