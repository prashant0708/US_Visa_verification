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