from dataclasses import dataclass

""" 
below mentioned class is just type hint , or class level variable which does
not accept the paramenter when it is called using instance because constractor is 
not available so if we use Abstraction class of dataclass , python automatically 
create constructor
"""

@dataclass
class DataIngestionArtifact:
    Train_file_path:str 
    Test_file_path:str 

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path:str
    transformed_test_file_path:str
    transformed_object_file_path:str


@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    trainer_model_S3_Bucket:str
    metric_artifact:ClassificationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    Accepted_model_accuracy:float
    S3_model_path:str
    trained_model_path:str
    trainer_model_s3_buckt_name:str

@dataclass
class ModelPusherArtifact:
    Model_Pusher_Bucket_Name : str 
    S3_Key_Model_Pusher_Path :str