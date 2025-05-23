from us_visa.constants import *
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.utils.main_utils import *
from us_visa.configuration.aws_config import S3Client
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.entity.estimator import USVisaModel
from sklearn.metrics import f1_score
from dataclasses import dataclass
from us_visa.entity.estimator import TargetValueMapping

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score:float
    best_model_f1_score:float
    is_model_accepted:bool
    f1_score_difference:float


class ModelEvaluation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig):
        

        logging.info("Model Evaluation is started")
        try:
            self.data_transformation_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evaluation_config = model_evaluation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH) ## this requird to access the drop columns name that need to remove from Test data.
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)

    def get_best_model(self):
        """
        Method Name: get_best_model
        Description : This function is used to get model from production
        Output: Return the model object if available in the S3 Storage
        On Failure :  Write a exception logs and raise exception
        """

        try:
            bucket_name = self.model_evaluation_config.bucket_name
            model_path =self.model_evaluation_config.s3_model_key_path
            usvisa_estimator = USVisaEstimator(Bucket=bucket_name,
                                               model_path=model_path)
            is_model_available=usvisa_estimator.is_model_present(model_path=model_path)
            if is_model_available:
                logging.info(f"Model available in S3 Bucket {is_model_available}")
                return usvisa_estimator.load_model()
            return None
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def evaluate_model(self):
        """
        Method Name : Evaluate Model
        description : This method is used to evaluate the trained model and production
                      model and choose the best one.
        output : return the bool value based on the result
        on failure : Write the exception log and then raise Exception log.
        """
        try:
            test_file_path = self.data_transformation_artifact.Test_file_path
            logging.info("taking the train path for the model evaluation")
            load_test_csv = load_data_from_s3(Bucket=BUCKET_NAME,Path=test_file_path,S3Client=S3Client)
            test_df = read_data(io.StringIO(load_test_csv))
            logging.info("Test data reading completed from the s3 bucket using Pandas")

            ## calculate the age of company
            test_df["company_age"] = CURRENT_YEAR-test_df['yr_of_estab']

            ## remove the Target column from x data
            x = drop_columns(df=test_df,cols=TARGET_COLUMN)
            ## remove the other two columns that is case_id and yr_of_estb from it
            drop_column = self.schema_config['drop_columns'] ## will return in list
            x_test = drop_columns(df=x,cols=drop_column)
            ## keep only target columns in y data
            y = test_df[TARGET_COLUMN]
            y_test = y.replace(TargetValueMapping().asdict())
            
            trainer_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"Trained model f1 score is {trainer_model_f1_score}")
            best_model_f1_score = None  # we have yet to calculate which model is best trained model or Production model so best model is None
            best_model = self.get_best_model()
            logging.info("getting the best model from Production s3 bucket{best_model}")


            if best_model is not None:
                y_hat_best_model = best_model.predict(x_test)
                best_model_f1_score = f1_score(y_test,y_hat_best_model)

            if best_model_f1_score is None:
                temp_best_f1_score =0
            else:
                temp_best_f1_score=best_model_f1_score
            result = EvaluateModelResponse(
                trained_model_f1_score=trainer_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted= trainer_model_f1_score>temp_best_f1_score,
                f1_score_difference=trainer_model_f1_score-temp_best_f1_score)
            logging.info(f"Result of the Model Evaluation is {result}")
            logging.info("Model evaluation is completed")
            return result
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def initiate_model_evaluation(self):
        """  
        This method is initiate the model evaluation process. 
        """
        try:
            model_evaluation_response=self.evaluate_model()
            s3_model_path = self.model_evaluation_config.s3_model_key_path
            trained_model_path= self.model_trainer_artifact.trained_model_file_path
            trainer_model_s3_bucket = self.model_trainer_artifact.trainer_model_S3_Bucket
            trainer_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            evaluation_result = self.evaluate_model()

            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=model_evaluation_response.is_model_accepted,
                                                                Accepted_model_accuracy=trainer_model_f1_score,
                                                                S3_model_path=s3_model_path,
                                                                trained_model_path=trained_model_path,
                                                                trainer_model_s3_buckt_name = trainer_model_s3_bucket)
            
            logging.info(f"Here is the Model evaluation Artifact{model_evaluation_artifact}")
            logging.info("Model evaluation completed")
            return model_evaluation_artifact
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
    