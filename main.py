from networksecurity.componants.data_ingestion import DataIngestion
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.ConfigEntity import DataIngestionConfig, TrainingPipelineConfig
import sys


if __name__ == '__main__':
    
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)