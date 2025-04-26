

class DataIngestionArtifact:
    Train_file_path:str 
    Test_file_path:str 


class DataValidationArtifact:
    validation_status:bool
    message:str
    drift_report_file_path:str