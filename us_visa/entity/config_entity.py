from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION



class TrainingPipeLineConfig:
    root_dir = ROOT_DIR
    pipeline_name = PIPELINE_NAME
    artifact_dir = os.path.join(root_dir,ARTIFACT_DIR_NAME,pipeline_name)
    
    


training_pipeline_config : TrainingPipeLineConfig=TrainingPipeLineConfig()


class DataIngestionConfig:
    data_ingestion_dir_path = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    raw_file_dir_path = os.path.join(data_ingestion_dir_path,CURRENT_TIME_STEMP,RAW_FILE_DIR)
    raw_data_file_path = os.path.join(raw_file_dir_path,RAW_DATA)
    splited_file_dir_path = os.path.join(data_ingestion_dir_path,CURRENT_TIME_STEMP,SPLITED_FILE_DIR)
    training_file_path = os.path.join(splited_file_dir_path,TRAIN_DATA)
    testing_file_path = os.path.join(splited_file_dir_path,TEST_DATA)

    
