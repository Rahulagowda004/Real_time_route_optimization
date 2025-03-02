import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from dataclasses import dataclass
from geopy.distance import geodesic
from src.utils.exception import CustomException
from src.utils.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts/Data',"train.csv")
    test_data_path: str=os.path.join('artifacts/Data',"test.csv")
    raw_data_path: str=os.path.join('artifacts/Data',"dataset.csv")

class DataIngestion:
    def __init__(self):
        
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        
        def create_delivery_features(df_features):
            
            avg_delivery_time_area = df_features.groupby('City')['Time_taken'].mean().to_dict()

            traffic_weather_impact = (
                df_features.groupby(['Road_traffic_density', 'Weatherconditions'])['Time_taken'].mean().to_dict()
            )

            # Maximum deliveries by vehicle type for capacity utilization
            max_deliveries_per_vehicle = (
                df_features.groupby('Type_of_vehicle')['multiple_deliveries'].max().to_dict()
            )
        
            def calculate_distance(row):
                restaurant_coords = (row['translogi_latitude'], row['translogi_longitude'])
                delivery_coords = (row['Delivery_location_latitude'], row['Delivery_location_longitude'])
                return geodesic(restaurant_coords, delivery_coords).kilometers
            
            df_features['avg_delivery_time_area'] = df['City'].map(avg_delivery_time_area)
    
            # Map traffic and weather impact
            df_features['traffic_weather_impact'] = df.apply(
                lambda row: traffic_weather_impact.get((row['Road_traffic_density'], row['Weatherconditions']), None),
                axis=1
            )
            
            # Calculate vehicle capacity utilization
            df_features['vehicle_capacity_utilization'] = df.apply(
                lambda row: row['multiple_deliveries'] / max_deliveries_per_vehicle.get(row['Type_of_vehicle'], 1),
                axis=1
            ).fillna(0)
            
            df_features['distance'] = df_features.apply(calculate_distance, axis=1)
            os.makedirs('artifacts/preprocessor/', exist_ok=True)
            joblib.dump(avg_delivery_time_area, 'artifacts/preprocessor/avg_delivery_time_area.pkl')
            joblib.dump(traffic_weather_impact, 'artifacts/preprocessor/traffic_weather_impact.pkl')
            joblib.dump(max_deliveries_per_vehicle, 'artifacts/preprocessor/max_deliveries_per_vehicle.pkl')
            
            return df_features

        print("************Initialized Data Ingestion************")
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv(self.ingestion_config.raw_data_path)
            df = df.copy()
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            def clean_df(df):
                df.drop(['ID'], axis=1, inplace=True) #dropping the ID column(irrelavant)
                df['Order_Date']=pd.to_datetime(df['Order_Date'])
                df['Order_day']=df['Order_Date'].dt.day
                df['Order_month']=df['Order_Date'].dt.month
                df['Order_year']=df['Order_Date'].dt.year
                df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'])
                df['Hour_order']=df['Time_Orderd'].dt.hour
                df['Min_order']=df['Time_Orderd'].dt.minute
                df.drop(["Time_Orderd", "Order_Date"],axis = 1, inplace= True)
                # df['City'] = df['City'].fillna("unknown")
                df = create_delivery_features(df)
                
                return df
            
            df = clean_df(df)
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data iss completed")
            
            print("***********Ended Data Ingestion*******************")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    
    train_arr = pd.DataFrame(train_arr)
    test_arr = pd.DataFrame(test_arr)
    train_arr.to_csv("train_arr.csv",index=False,header=True)
    test_arr.to_csv("test_arr.csv",index=False,header=True)
    
    # modeltrainer=ModelTrainer()
    # print(modeltrainer.initiate_model_trainer(train_arr,test_arr))