import os
import sys
import numpy as np
import dill
import pickle
import yaml
from pandas import DataFrame
import pandas as pd

from us_visa.logger import logging
from us_visa.exception import USVISAEXCEPTION
import io

### READ_YAMLFILE FUNCTION 

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
    
## function to write yaml file

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        
        with open(file_path,"w") as file:
            yaml.dump(content,file)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
def write_yaml_file_s3(content:object,memory_path)->None:
    try:
        if memory_path:
            yaml.dump(content,memory_path)
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e

    
## function to load the object

def load_object(file_path:str) ->object:
    logging.info("Entered the load_object method of utils")
    
    try:
        with open(file_path,"rb") as file_obj:
            obj = dill.load(file_obj)
        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
###  function save the object
def save_object(file_path:str , obj:object)->None:
    logging.info("Entred the save_object method of utils")
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    

## save object to the S3

def save_object_s3(obj:object)->io:
    """ 
    save object to s3
    
    array: np.array data to save
    """
    try:
        buffer = io.BytesIO()
        dill.dump(obj,buffer)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise USVISAEXCEPTION(e,sys)
    
def load_object_s3(s3,key,Bucket)->object:
    try:
        response = s3.s3_client.get_object(Bucket=Bucket , Key=key)
        body = response['Body'].read()
        obj = dill.load(io.BytesIO(body))
        return obj
    except Exception as e:
        raise USVISAEXCEPTION(e,sys)


def save_numpy_array_data(file_path:str , array : np.array)->None:
    """ 
    save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok= True)
        
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
def save_numpy_array_data_s3(array : np.array)->io:
    """ 
    save numpy array data to s3
    
    array: np.array data to save
    """
    try:
        buffer = io.BytesIO()
        np.save(buffer,array)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
### load the numpy array

def load_numpy_array_data (file_path:str)-> np.array:
    try:
        with open(file_path , 'rb') as file_obj:
            return np.load(file_obj)
        logging.info(f"array data read by np from location {file_path}")
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    
def load_numpy_array_data_s3(s3,key,Bucket)->np.array:
    """   
    This method is to load the numpy array from the S3 Bucket
    """
    try:
        response = s3.s3_client.get_object(Bucket = Bucket,Key=key)
        array = np.load(io.BytesIO(response['Body'].read()))
        return array
    except Exception as e:
        raise USVISAEXCEPTION(sys,e)
    
## function to drop the columns

def drop_columns(df:DataFrame,cols:list)->DataFrame:
    try:
        df = df.drop(columns=cols,axis=1)
        logging.info("Exited the drop_columns method of utils")
        return df
    except Exception as e:
        raise USVISAEXCEPTION(e,sys) from e
    

### function to read the data and return the dataframe

def read_data(file_path:str) -> DataFrame:
    try:
        # if file_path.endswith('.csv'):
        #     return pd.read_csv(file_path)
        # elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        #     return pd.read_excel(file_path)
        # elif file_path:
        #     return pd.read_csv(file_path)
        # else:
        #     logging.inf("File is not in correct formate")
        return pd.read_csv(file_path)
    except Exception as e:
        USVISAEXCEPTION(sys,e)


## load the data from S3

def load_data_from_s3(Bucket:str,Path:str,S3Client:object):
    try:
        S3_Client = S3Client()
        response = S3_Client.s3_client.get_object(Bucket=Bucket,Key=Path)
        content =response['Body'].read()
        csv_buffer = content.decode('utf-8')
        return csv_buffer
    except Exception as e:
        USVISAEXCEPTION(sys,e)

def load_data_to_s3(Bucket:str,path:str,S3Client:object,Body):
    try:
        S3_Client = S3Client()
        S3_Client.s3_client.put_object(Bucket=Bucket,Key=path,Body=Body)
    except Exception as e:
        USVISAEXCEPTION(sys,e)






    


        
    
    

