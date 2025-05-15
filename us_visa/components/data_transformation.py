import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer
from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
from us_visa.constants import *
from us_visa.utils.main_utils import *
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact)
from us_visa.entity.estimator import TargetValueMapping
from us_visa.configuration.aws_config import S3Client



class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,
                       data_ingestion_artifact:DataIngestionArtifact,
                       data_validation_artifact:DataValidationArtifact):
        
        """
        Param: Data Ingestion Artifact : Output of Data Ingestion Process
        Param: Data Validation Artifact: Output of Data Validation Process
        Param: Data Transformation Config : Configuration file of Data Transformation  
        
        """
        try:
            
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            self.s3client= S3Client()
            
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def get_data_transformation_object(self)->Pipeline:
        """
        Method Name :   get_data_transformation_object
        Description :   This method return the pipeline of the Data Transformation
        
        Output      :   Data Transformation Object is created and returned
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Data Transformation Object /Pipeline creation Started")
        try:

            Numerical_Transformer =StandardScaler()
            oh_transformer = OneHotEncoder()
            or_transformer = OrdinalEncoder()

            logging.info("Intilized StandardScaler,OneHotEncoder,OrdinalEncoder")

            transform_column = self.schema_config['transform_columns']
            oh_columns       = self.schema_config['oh_columns']
            or_columns       = self.schema_config['or_columns']
            num_features     = self.schema_config['num_features']
            logging.info(f"""one_hot_columns: [{oh_columns}] ,
                        ordinal_columns:[{or_columns}],
                        Numerical_columns : [{num_features}],
                        transform_column  : [{transform_column}]
                        all the columns are accessed from schema.yaml to transform
                        """)
            
            transformer = Pipeline(steps=[('transformer',
                                            PowerTransformer(method='yeo-johnson'))])
            
            preprocessor = ColumnTransformer(
                [
                            ('OrdinalEncoder',or_transformer,or_columns),
                            ('OneHotEncoder',oh_transformer,oh_columns),
                            ('Transformer',transformer,transform_column),
                            ('StandardScaler',Numerical_Transformer,num_features)
    
                ])
            
            logging.info("Created the preprocessing object using ColumnTransformer")
            logging .info("Preprocessing object creation Completed")
            return preprocessor
        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        
    def initiate_data_transformer(self)-> DataTransformationArtifact:
        """ 
        Method :initiate_data_transformer
        Description : This Process will apply Data Transformation object on train and test data
        Output:" Transformed Train and Test Data"
        On Failure: Write a exception log and raise Exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Data Transformation Started")
                train_filePath =self.data_ingestion_artifact.Train_file_path
                logging.info("Got the training data")
                test_filePath = self.data_ingestion_artifact.Test_file_path
                logging.info("Got the test data")
                preprocessing = self.get_data_transformation_object()
                logging.info("Got the preprocessing Object")
                load_train_csv = load_data_from_s3(Bucket=BUCKET_NAME,Path=train_filePath,S3Client=S3Client)
                logging.info("Train data StreamingBody  got from the s3 bucket ")
                load_test_csv = load_data_from_s3(Bucket=BUCKET_NAME,Path=test_filePath,S3Client=S3Client)
                
                logging.info("Train data StreamingBody  got from the s3 bucket ")
            
                train_df = read_data(io.StringIO(load_train_csv))
                logging.info("Training df created")
                test_df = read_data(io.StringIO(load_test_csv))
                logging.info("Testing df created")

                ## split the train data into Independent and Target variable
                ## On Train data set 
                input_feature_train_df = drop_columns(df=train_df,cols=[TARGET_COLUMN]) ## removing the target columns from the train dataset
                target_feature_train_df = train_df[TARGET_COLUMN]
                input_feature_train_df["company_age"] = CURRENT_YEAR-input_feature_train_df['yr_of_estab']
                drop_column= self.schema_config['drop_columns']
                input_feature_train_df = drop_columns(df=input_feature_train_df,cols=drop_column)
                logging.info(f"{drop_column} are dropped from the train dataframe")

                target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().asdict())
                

                ## on test dataset
                input_feature_test_df = drop_columns(df=test_df,cols=[TARGET_COLUMN]) ## removing the target columns from the train dataset
                target_feature_test_df = test_df[TARGET_COLUMN]
                input_feature_test_df["company_age"] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                
                input_feature_test_df = drop_columns(df=input_feature_test_df,cols=drop_column)
                logging.info(f"Test data {drop_column} columns are dropped")
                target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().asdict())

                logging.info("Train and Test data set got for preprocessing object")

                ## Preprocessing
                input_feature_train_arr = preprocessing.fit_transform(input_feature_train_df)
                logging.info("Data transformationof train input is done")

                input_feature_test_arr = preprocessing.transform(input_feature_test_df)
                logging.info("Data transformationof test input is done")

                ## smoothing
                logging.info("Applying the smoothing on train dataset")

                smt = SMOTEENN(sampling_strategy="minority")

                input_feature_train_final,target_feature_train_final=smt.fit_resample(input_feature_train_arr,target_feature_train_df)
                logging.info("Smoothing on train input and target are completed")

                logging.info("Applying the smoothing on test dataset")
                input_feature_test_final,target_feature_test_final=smt.fit_resample(input_feature_test_arr,target_feature_test_df)
                logging.info("Smoothing on test input and target are completed")

                ## Creating Train and test array

                logging.info("Creating the train array and test array ")
                train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
                test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]
                logging.info("Created the train array and test array ")
                logging.info("saving all the array in location ")

                #save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)

                buffer_value= save_numpy_array_data_s3(train_arr)
                load_data_to_s3(Bucket=BUCKET_NAME,path=self.data_transformation_config.transformed_train_file_path,
                                S3Client=S3Client,Body=buffer_value)


                logging.info(f"Training array saved at [{self.data_transformation_config.transformed_train_file_path}]")

                #save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)

                buffer_value= save_numpy_array_data_s3(test_arr)
                load_data_to_s3(Bucket=BUCKET_NAME,path=self.data_transformation_config.transformed_test_file_path,
                                S3Client=S3Client,Body=buffer_value)

                logging.info(f"Test array saved at [{self.data_transformation_config.transformed_test_file_path}]")


                #save_object(self.data_transformation_config.transformed_object_file_path,preprocessing)
                buffer_obj=save_object_s3(preprocessing)
                load_data_to_s3(Bucket=BUCKET_NAME,path=self.data_transformation_config.transformed_object_file_path,
                                S3Client=S3Client,Body=buffer_obj)


                logging.info(f"preprocessing object  saved at [{self.data_transformation_config.transformed_object_file_path}]")

                data_transformation_artifact  = DataTransformationArtifact(transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                        transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                                                                        transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
                                                                        
                                                                        )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.validation_status)

        except Exception as e:
            raise USVISAEXCEPTION(sys,e)
        



        