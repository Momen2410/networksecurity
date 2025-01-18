import os
import sys
import numpy as np
import pandas as pd


'''
define common constant variables for training pipeline
'''

TARGET_COULMNS: str = 'Result'
PIPLINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR: str = 'Artifact'
FILE_NAME: str = 'phisingData.csv'

TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

'''
Data Ingestion related constant start with DATA_INGESTION VAR NAME
'''
DATA_INGESTION_COLLECTION_NAME: str = 'PhishingData'
DATA_INGESTION_DATABASE_NAME: str = 'MomenAI'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

