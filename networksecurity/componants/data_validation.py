from networksecurity.entity.DataIngestionEntity import DataIngestionArtifacts, DataValidationArtifacts
from networksecurity.entity.ConfigEntity import DataValidationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
from networksecurity.constants import training_pipeline
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.MainUtils import read_yaml_file, write_yaml_file
import os, sys
import pandas as pd

class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
                 data_ingestion_artifacts: DataIngestionArtifacts):
        
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def detect_dataset_drift(self, base_df, current_df, threshhold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                if threshhold <= is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({column:{
                    "drift_status": is_found,
                    "p_value": float(is_sample_dist.pvalue)
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            
            ## create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifacts.train_path
            test_file_path = self.data_ingestion_artifacts.test_path
            
            ## read data from files 
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            ## validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe dose not contains all columns. \n"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe dose not contains all columns. \n"
                
            ## Check datadrift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=False
            )
            
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=False
            )
            
            data_validation_artifact = DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifacts.train_path,
                valid_test_file_path=self.data_ingestion_artifacts.test_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                
            )
            return data_validation_artifact
                
        except Exception as e:
            raise NetworkSecurityException(e, sys)