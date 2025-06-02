from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.configuration.aws_config import S3Client
from us_visa.entity.config_entity import ModelMonitortingConfig
from us_visa.entity.artifact_entity import ModelPusherArtifact,DataIngestionArtifact
from pandas import DataFrame
import json
from evidently import Report
from evidently.presets import DataDriftPreset
from us_visa.utils.main_utils import *
from us_visa.constants import *
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.entity.estimator import USVisaModel
from sklearn.metrics import f1_score

S3_Client=S3Client()

## i want to download the data from s3 training data 

## i want to load the production model from s3 
## i have prediction data 
## first i will check the data drift and model performance based on that 
## if model accuracy is less that 90% then i will retrain the model

class ModelMonitoring:
    def __init__(self,model_monitoring_config:ModelMonitortingConfig,data_ingestion_artifact:DataIngestionArtifact):
        self.model_monitoring_config=model_monitoring_config
        self.data_ingestion_artifact=data_ingestion_artifact
        
    def detect_data_drift(self,df_1:DataFrame,df_2:DataFrame)->bool:
        """ 
        Method Name : detect data drift
        description : Detect the data drift by comparing the train and test data 
        Output : Return the Boolen value based on the drift check
        On Failure : Write a log file and raise exception
        """
        try:
            logging.info("Data Drift checking started")
            monitoring_bucket= self.model_monitoring_config.monitoring_bucket
            
            data_drift_profile = Report([DataDriftPreset()])
            data_drift_report =data_drift_profile.run(df_1,df_2)
            report = data_drift_report.json()
            json_report = json.loads(report)
            metrics = json_report["metrics"]
            if self.data_validation_config.data_validation_drift_report_dir_name:
                yaml_buffer = io.StringIO()
                #yaml.dump(json_report,yaml_buffer)
                write_yaml_file_s3(json_report,yaml_buffer)
                load_data_to_s3(Bucket=monitoring_bucket,path=self.model_monitoring_config.model_monitoring_path,
                                S3Client=S3Client,
                                Body=yaml_buffer.getvalue()
                                )
                logging.info("Model Monitoring yaml file store in S3 Bucket")
                #write_yaml_file(self.data_validation_config.data_validation_drift_report_file_path,content=json_report)
            else:
                logging.info(f"Path not exists: [{self.model_monitoring_config.model_monitoring_path}]")
            #n_features = json_report["metrics"][0]["result"]["n_features"]
            feature=[]
            for i in metrics:
                col =i["metric_id"].split("column=")[-1].split(")")[0]
                feature.append(col)
            n_features=len(feature[1:])

            #n_drifted_feature = json_report["metrics"][0]["result"]["n_drifted_features"]
            n_drifted_feature=metrics[0]['value']['count']
            logging.info(f"{n_drifted_feature}/{n_features} drift detected")

            #drift_status = json_report["metrics"][0]["result"]["dataset_drift"]
            drift_status=metrics[0]['value']['share']
            return drift_status
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def get_production_model(self):
        """
        Method Name: get model from the s3
        Description : This function is used to get model from production
        Output: Return the model object if available in the S3 Storage
        On Failure :  Write a exception logs and raise exception
        """
        try:
            bucket_name = MODEL_BUCKET_NAME
            model_path = MODEL_FILE_NAME
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
        
        try: 
            predicted_data_path = self.model_monitoring_config.predicted_data_path
            df = pd.read_csv(predicted_data_path)
            avg_prediction_time = df["prediction_time"].mean()
            x = drop_columns(df=df,cols=["prediction_time","prediction"])
            y = df["prediction"]
            
            model = self.get_production_model()
            
            y_hat = model.predict(x)
            model_f1_score = f1_score(y,y_hat)
            
            logging.info(f"Prodcution model f1 score and avg prediction time {model_f1_score,avg_prediction_time}")
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def initiate_model_monitoring(self):
        predicted_data_path = self.model_monitoring_config.predicted_data_path
        df = pd.read_csv(predicted_data_path)
        df = drop_columns(df=df,cols=["prediction"])
        load_train_csv = load_data_from_s3(Bucket=BUCKET_NAME,Path=self.data_ingestion_artifact.Train_file_path,S3Client=S3Client)
        logging.info("Train CSV Buffer from IO created")

        train_df = read_data(io.StringIO(load_train_csv))
        logging.info("Training data read from s3")
        print(train_df.head())
        print(df.head())
        
        #self.detect_data_drift(df_1=df,df_2= train_df)
        self.evaluate_model()
        
        
            
        
