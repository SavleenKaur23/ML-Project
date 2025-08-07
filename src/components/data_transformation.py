import sys
import os
from dataclasses import dataclass # decorator

import pandas as pd
import numpy as np 

#from sklearn.model_selection import 
from sklearn.compose import ColumnTransformer  # creating pipelines
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object  #saving the pickle file

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')  #model file: pickle file - binary file to save and reload Python objects, commonly for storing trained ML models

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):  #create all pickle file 
        '''
        Function for handling Data Transformation
        '''
        try:
            numerical_features = ["reading score", "writing score"]
            categorical_features = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())  
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()) ,
                    ('scaler',StandardScaler(with_mean=False))  
                ]
            )
            
            logging.info(f"Numerical Columns: {numerical_features}")
            logging.info(f"Categorical Columns: {categorical_features}")

            logging.info("Std Scaling for Numerical features completed")
            logging.info("Encoding and Std Scaling for Categorical features completed")
            
            preprocessor = ColumnTransformer(
                [
                    ("Numerical Pipeline", numerical_pipeline,numerical_features),
                    ("Categorical Pipeline", categorical_pipeline,categorical_features)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading of Train and Test Data is completed")
            logging.info("obtaining preprocessing object")

            preprocessor_obj = self.get_data_transformer_object()
            # preprocessing object needs to be converted to pickle file
            # we have the path above DataTransformationCOnfig as preprocessor_obj_file_path

            target_column = 'math score'
            numerical_features = ['reading score', 'writing score',]

            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]
            
            logging.info(f"Applying preprocessing object on training dataframe and test dataframe")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            # column-wise concatenation i.e combining the transformed features with the target column(s) to create a final array.
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info(f"Saved Preprocessing Object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr,test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            #preprocessing object needs to be converted to pickle file
            
            
            #so we are going to save it in utils as this save common functionalities

        except Exception as e:
            raise CustomException(e,sys)

