import os
import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,RobustScaler,MinMaxScaler,StandardScaler
from src.components.custom_transformer import FilterOutBigValuesTransformer
from src.utils.exception import CustomException
from src.utils.logger import logging
from src.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts/preprocessor',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        
    def get_data_transformer_object(self):
        try:
            mean_features = ['Delivery_person_Age', 'Delivery_person_Ratings', 'multiple_deliveries', 'Hour_order', 'Min_order']
            ohe_categories = ['Road_traffic_density', 'Type_of_vehicle']
            ordinal_categories = ['Road_traffic_density', 'Weatherconditions', 'Type_of_vehicle', 'City']
            robust_features = ['translogi_latitude', 'translogi_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            standardize_features = ['Temperature', 'Traffic_Index', 'Delivery_person_Age', 'Delivery_person_Ratings']
            
            mean_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ohe', OneHotEncoder(handle_unknown='ignore'))
            ])

            ordinal_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ordinal', OrdinalEncoder()),
                ('scaler', RobustScaler())
            ])

            num_pipeline_standardize = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),  
                ('scaler', StandardScaler())  
            ])

            num_pipeline_robust = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', RobustScaler())
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_mean', mean_pipeline, mean_features),
                    ('num_standardize', num_pipeline_standardize, standardize_features),
                    ('num_robust', num_pipeline_robust, robust_features),
                    ('cat', cat_pipeline, ohe_categories),
                    ('ordinal', ordinal_pipeline, ordinal_categories),
                ])

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            print("**********Initialized Data Transformation*********")
            
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="Time_taken"

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            
            print("*************Ended Data Transformation************")
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)