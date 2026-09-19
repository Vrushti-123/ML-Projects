# read the data from a particulare ource, be it local source, mongoDB etc.

import os # for operating-system-related tasks --> path.join(), makedirs
import sys # Used to access information about the Python runtime.
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass #important!!!

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass #decorator
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv") #trained data --> shown in this path
    # so basically, an "artifact" folder gets created, and inside that train.csv gets created for storing our train data.
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")
    # now data ingestion component knows where to save the train path, test path and data path
        
class DataIngestion:
    # Its responsibility is basically:
    # Get the raw data, save it, split it, and save the split datasets.
    
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        # DataIngestionConfig class contains 3 objects --> train_data_path, test_data_path, raw_data_path
        # so now, ingestion_config contains all these three now too.
        # so, self.ingestion_config.train_data_path contains that class's train data path.

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # creates "artifacts" folder if it doesn't already exist.

            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
                )
            # This is basically keeping a copy of the raw dataset inside your artifacts directory.
            # our raw data --> stored in "df".

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            # it splits df and stores into train_set and test_set.

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # stores our train data inside artifacts/train.csv

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            # stores our test data inside artifacts/test.csv
                        
            logging.info("Ingestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        # so whenever we call obj.initiate_data_ingestion() --> we get train_data and test_data.

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))


# ---------------------------------------------------------------------------------------
'''
With @dataclass

You can simply write:

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

Python automatically generates the necessary __init__() for you.
Conceptually, Python treats it roughly like:

class DataIngestionConfig:
    def __init__(
        self,
        train_data_path=os.path.join('artifacts', 'train.csv'),
        test_data_path=os.path.join('artifacts', 'test.csv'),
        raw_data_path=os.path.join('artifacts', 'data.csv')
    ):
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.raw_data_path = raw_data_path

The main benefit is:
You don't have to manually write boilerplate code for a class whose main purpose is storing data.
'''

'''     OVERALL FLOW:

                    ┌─────────────────────┐
                    │    stud.csv         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Ingestion    │
                    │                     │
                    │ read CSV            │
                    │ save raw data       │
                    │ train/test split    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              train.csv               test.csv
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Data Transformation │
                    │                     │
                    │ preprocessing       │
                    │ encoding            │
                    │ scaling             │
                    └──────────┬──────────┘
                               │
                         train_arr
                         test_arr
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Model Trainer    │
                    │                     │
                    │ train models        │
                    │ evaluate models     │
                    │ save best model     │
                    └─────────────────────┘
'''


''' DATA INGESTION FLOW:
                    ┌─────────────────────────┐
                    │       stud.csv          │
                    │  notebook/data/stud.csv │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     DataIngestion       │
                    │                         │
                    │  DataIngestionConfig    │
                    │          ↓              │
                    │  define file paths      │
                    │                         │
                    │  read CSV using Pandas  │
                    │          ↓              │
                    │  create artifacts/      │
                    │          ↓              │
                    │  save raw data          │
                    │          ↓              │
                    │  train/test split       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │  train.csv   │          │   test.csv   │
             │     80%      │          │     20%      │
             └──────┬───────┘          └──────┬───────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Return file paths     │
                    │                         │
                    │ train_data =            │
                    │ "artifacts/train.csv"   │
                    │                         │
                    │ test_data =             │
                    │ "artifacts/test.csv"    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  DataTransformation     │
                    │                         │
                    │  read train/test data   │
                    │          ↓              │
                    │  imputation             │
                    │  encoding               │
                    │  scaling                │
                    │          ↓              │
                    │  train_arr              │
                    │  test_arr               │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      ModelTrainer       │
                    │                         │
                    │  train ML models        │
                    │          ↓              │
                    │  evaluate models        │
                    │          ↓              │
                    │  select model           │
                    │          ↓              │
                    │  save trained model     │
                    └─────────────────────────┘

'''