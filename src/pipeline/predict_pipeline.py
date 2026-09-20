import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        # features --> contains the new student's data like gender, race, education etc.
        # features are passed in the form of a dataframe.
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
             # we have already created these, just have to load them now
            print("Before Loading")

            model=load_object(file_path=model_path) #final trained model on best alg and params
            preprocessor=load_object(file_path=preprocessor_path) 
            # preprocessing_obj --> (instance of final pipeliined/transformed result)
            print("After Loading")

            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        # predicted value is returned to whoever calls predict() 
        
        except Exception as e:
            raise CustomException(e,sys)



# Its purpose is:
# Take the values entered by the user and convert them into 
# the exact DataFrame format expected by your ML pipeline.
class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)

'''
             USER ENTERS DATA
                    │
                    ▼
            ┌───────────────┐
            │  CustomData   │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │   DataFrame   │
            └───────┬───────┘
                    │
                    ▼
       ┌────────────────────────┐
       │     preprocessor.pkl   │
       │                        │
       │ transform()            │
       │ • imputation           │
       │ • encoding             │
       │ • scaling              │
       └───────────┬────────────┘
                   │
                   ▼
          Processed numerical data
                   │
                   ▼
          ┌─────────────────┐
          │    model.pkl    │
          │                 │
          │  model.predict  │
          └────────┬────────┘
                   │
                   ▼
          Predicted Math Score
'''