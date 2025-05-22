from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import ModelEvaluationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from us_visa.configuration.aws_config import S3Client
from us_visa.entity.s3_estimator import USVisaEstimator
import sys


class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,model_pusher_config:ModelPusherConfig):
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.S3 = S3Client()
        self.usvisaestimator = USVisaEstimator(Bucket=model_pusher_config.Model_Pusher_Bucket_Name,
                                               model_path=model_pusher_config.S3_Key_Model_Pusher_Path)
        
    def initiate_model_pusher(self):
        logging.info("Entered to the Initiate model_pusher")
        try:
          # self.model_evaluation_artifact.trained_model_path
            self.usvisaestimator.save_model(source_bucket=self.model_evaluation_artifact.trainer_model_s3_buckt_name,
                                            source_key=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(Model_Pusher_Bucket_Name=self.model_pusher_config.Model_Pusher_Bucket_Name,
                                                        S3_Key_Model_Pusher_Path=self.model_pusher_config.S3_Key_Model_Pusher_Path)
            logging.info(f"Model pusher artifact [{model_pusher_artifact}]")
            return model_pusher_artifact
            
            
        except Exception as e:
            raise USVISAEXCEPTION(e,sys) from e
        

    