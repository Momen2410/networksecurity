from networksecurity.componants.data_ingestion import DataIngestion
from networksecurity.componants.data_validation import DataValidation
from networksecurity.componants.data_transformation import DataTransformation

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.ConfigEntity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
import sys


if __name__ == '__main__':
    
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion succeeded")
        print(data_ingestion_artifact)
        data_validation=DataValidation(data_validation_config, data_ingestion_artifact)
        logging.info("Initiate Data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation succeeded")
        data_transformtion_config = DataTransformationConfig(training_pipeline_config)
        logging.info('data transformation started')
        data_transformation = DataTransformation(data_transformtion_config, data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info('Data transformation succeeded')
        print(data_transformation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)