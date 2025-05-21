from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.configuration.aws_config import S3Client
import posixpath
from dataclasses import dataclass



class S3Bucket:
    """ 
    This class will check if bucket is not exist than will create it  
    
    """
    def __init__(self,Bucket_name:str):
        self.s3client_class = S3Client()
        self.Bucket_name=Bucket_name
    def create_bucket(self):
        Existing_bucket = [bucket["Name"] for  bucket in self.s3client_class.s3_client.list_buckets()["Buckets"]]
        if self.Bucket_name not in Existing_bucket:
            if REGION  == CHECK_REGION:
                self.s3client_class.s3_client.create_bucket(Bucket = self.Bucket_name)
                return self.Bucket_name
                logging.info("Bucket at s3 created {self.Bucket_name}")
            else:
                localtion={'LocationConstraint':REGION}
                self.s3client_class.s3_client.create_bucket(Bucket = self.Bucket_name,
                                                CreateBucketConfiguration=localtion
                                                )
                return self.Bucket_name
                logging.info("Bucket at s3 created {self.Bucket_name} at location {localtion}")
            
        else:
            logging.info("Bucket exists {self.Bucket_name} at location {localtion}")
            return self.Bucket_name

# artifact_dir = posixpath.join(ARTIFACT_DIR_NAME,PIPELINE_NAME,CURRENT_TIME_STEMP)+"/"
# data_ingestion = posixpath.join(artifact_dir,DATA_INGESTION_DIR_NAME)+"/"

#s3cilent.s3_client.put_object(Bucket=Bucket_name,Key=data_ingestion)

class TrainingPipeLineConfig:
    root_dir = ROOT_DIR ##this is for local
    pipeline_name = PIPELINE_NAME 
    Current_time_stemp = CURRENT_TIME_STEMP
    #artifact_dir = os.path.join(ARTIFACT_DIR_NAME,pipeline_name,Current_time_stemp)
    artifact_dir = posixpath.join(ARTIFACT_DIR_NAME,PIPELINE_NAME,CURRENT_TIME_STEMP)+"/"

    
    


training_pipeline_config : TrainingPipeLineConfig=TrainingPipeLineConfig()


class DataIngestionConfig:
    data_ingestion_dir_path = posixpath.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)+"/"
    raw_file_dir_path = posixpath.join(data_ingestion_dir_path,RAW_FILE_DIR)+"/"
    raw_data_file_path = posixpath.join(raw_file_dir_path,RAW_DATA)
    splited_file_dir_path = posixpath.join(data_ingestion_dir_path,SPLITED_FILE_DIR)+"/"
    training_file_path = posixpath.join(splited_file_dir_path,TRAIN_DATA)
    testing_file_path = posixpath.join(splited_file_dir_path,TEST_DATA)

class DataValidationConfig:
    data_validation_dir_path = posixpath.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)+"/"
    data_validation_drift_report_dir_name = posixpath.join(data_validation_dir_path,DATA_VALIDATION_DRIFT_REPORT_DIR_NAME,CURRENT_TIME_STEMP)+"/"
    data_validation_drift_report_file_path = posixpath.join(data_validation_drift_report_dir_name,DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    data_transformation_dir_path = posixpath.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)+"/"
    data_transformation_transformed_data_dir = posixpath.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)+"/"
    data_transformation_transformed_object_dir = posixpath.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)+"/"
    transformed_train_file_path :str = posixpath.join(data_transformation_transformed_data_dir,DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME)
    transformed_test_file_path : str = posixpath.join(data_transformation_transformed_data_dir,DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME)
    transformed_object_file_path:str = posixpath.join(data_transformation_transformed_object_dir,PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    model_trainer_dir_path = posixpath.join(training_pipeline_config.artifact_dir,MODEL_TRAINER_DIR_NAME)+"/"
    model_trainer_trained_dir_path = posixpath.join(model_trainer_dir_path,MODEL_TRAINER_TRAINED_MODEL_DIR_NAME)+"/"
    model_trainer_trained_model_path = posixpath.join(model_trainer_dir_path,MODEL_TRAINER_TRAINER_MODEL_NAME)


class ModelEvaluationConfig:
    changed_threshould_score:float = MODEL_EVALUATION_CHNAGED_THRESHOLD_SCORE
    bucket_name :str = MODEL_BUCKET_NAME
    s3_model_key_path :str = MODEL_FILE_NAME

class ModelPusherConfig:
    Model_Pusher_Bucket_Name : str = MODEL_BUCKET_NAME
    S3_Key_Model_Pusher_Path :str = MODEL_FILE_NAME


@dataclass
class USvisaPredictorConfig:
    model_file_path: str = MODEL_FILE_NAME
    model_bucket_name: str = MODEL_BUCKET_NAME

    


    
