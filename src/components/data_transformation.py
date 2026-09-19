import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")
    # preprocessor_obj_file_path = artifacts/proprocessor.pkl --> created

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        # on getting called/initializing , DataTransformation calls DataTransformationConfig() 
        # and saves it inside self.data_transformation_config

    def get_data_transformer_object(self):
        # This function is responsible for data trnasformation
    
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                # An imputer is a tool used to fill in missing values in your dataset.
                # here, in place of missing values --> it puts median.
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        # returns this "preprocessor" (final column transformed pipelined result)
    
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()
            # preprocessing_obj --> (instance of final pipeliined/transformed result) --> to be used for training now.

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # the instance that was created earlier is used here.
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # np.c_ means concatenate columns.
            # input_feature_train_arr (X values ) --> contains transformed X values.
            # But: target_feature_train_df (Y values )--> still contains the original math_score.

            train_arr = np.c_[
                input_feature_train_arr, 
                np.array(target_feature_train_df)
            ]
            '''
            Transformed X_train       y_train
                    |                     |
                    |                     |
                    +----------+----------+
                                ↓
                            train_arr
            '''

            test_arr = np.c_[
                input_feature_test_arr, 
                np.array(target_feature_test_df)
            ]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
                # we're saving preprocessing_obj to artifacts/proprocessor.pkl
                # proprocessor.pkl contains the fitted preprocessing object.
            )

            return (
                train_arr, # X_train transformed + y_train
                test_arr, # X_test transformed + y_test
                self.data_transformation_config.preprocessor_obj_file_path, # Preprocessor path --> artifacts/proprocessor.pkl
            )
        
        # So another component, such as your training pipeline, can receive these.

        except Exception as e:
            raise CustomException(e,sys)


''' IMPUTATION METHOD:

Mean → affected by outliers.
Median → resistant to outliers.

| Data                                 | Use        |
| ------------------------------------ | ---------- |
| Roughly symmetric, no major outliers |   Mean     |
| Skewed data or has outliers          |   Median   |


'''

''' 
Part 1 — Build the recipe: 

get_data_transformer_object()

creates:

Numerical Pipeline
Categorical Pipeline
        ↓
ColumnTransformer

It essentially says:

"This is HOW I want my data transformed."
--------------------------------------------
Part 2 — Execute the recipe

initiate_data_transformation()
actually takes:

train.csv
test.csv

and runs that preprocessing.

get_data_transformer_object()
             ↓
      preprocessing_obj
             ↓
      fit_transform(X_train)
             ↓
      transform(X_test)

'''


''' OVERALL FLOW:

                 train.csv
                    |
                    ↓
              read with pandas
                    |
                    ↓
          Separate X and y
          /               \
         X                 y
         |
         ↓
  ColumnTransformer
         |
    +----+----+
    |         |
    ↓         ↓
Numerical   Categorical
Pipeline    Pipeline
    |         |
    ↓         ↓
Median      Most Frequent
Imputer     Imputer
    ↓         ↓
Scaler      OneHotEncoder
              ↓
            Scaler
    |         |
    +----+----+
         |
         ↓
   transformed X_train
         |
         +------ y_train
         |
         ↓
      train_arr
'''