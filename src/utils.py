import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    # the place where you want to save your object.
    # The Python object you want to save.

    try:
        dir_path = os.path.dirname(file_path)
        # get the folder from the file path.
        # file_path = "artifacts/model.pkl" --> Then "os.path.dirname(file_path)"" returns artifacts

        os.makedirs(dir_path, exist_ok=True)
        # This creates the directory if it doesn't already exist.

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            # pickle.dump(obj, file_obj) This takes Python object and serializes it into binary file.

    except Exception as e:
        raise CustomException(e, sys)

'''
save_object("artifacts/model.pkl", model)

means:
Save this model as model.pkl inside the artifacts folder.
'''
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    # Its job is basically: Take multiple ML models, 
    # find their best hyperparameters, train them, evaluate them, and return their scores.
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

        '''
            {
                "Linear Regression": 0.82,
                "Random Forest": 0.87,
                "Decision Tree": 0.75
            }
        
            Then the training pipeline can choose the model based on these scores.
        '''
        
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
        # It takes the location of a saved object.
        # Then reconstructs the Python object from the pickle file.

    except Exception as e:
        raise CustomException(e, sys)


'''
                 ML TRAINING
                     │
                     ▼
             evaluate_models()
                     │
          ┌──────────┴──────────┐
          │                     │
      Model 1                Model 2
          │                     │
     GridSearchCV          GridSearchCV
          │                     │
     Best params           Best params
          │                     │
          └──────────┬──────────┘
                     ▼
                Best model
                     │
                     ▼
               save_object()
                     │
                     ▼
              model.pkl
                     │
                     │
              Later / Prediction
                     │
                     ▼
               load_object()
                     │
                     ▼
               trained model
                     │
                     ▼
                 predict()
'''
 