import os
import sys
from src.utils.exception import CustomException
from src.utils.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"Dataset.csv")

class DataIngestion:
    def __init__(self):
        
        self.ingestion_config=DataIngestionConfig()
        
    def create_delivery_features(self,df_features):
        
        df_features['avg_delivery_time_area'] = df_features.groupby('City')['Time_taken'].transform('mean')

        df_features['traffic_weather_impact'] = df_features.groupby(
            ['Road_traffic_density', 'Weatherconditions']
        )['Time_taken'].transform('mean')

        df_features['vehicle_capacity_utilization'] = (
            df_features['multiple_deliveries'] / 
            df_features.groupby('Type_of_vehicle')['multiple_deliveries'].transform('max')
        ).fillna(0)
        
        return df_features

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv(self.ingestion_config.raw_data_path)
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.drop(['ID'], axis=1, inplace=True) #dropping the ID column(irrelavant)
            
            df['Order_Date']=pd.to_datetime(df['Order_Date'])

            # Creating three column for day,month and year
            df['Order_day']=df['Order_Date'].dt.day
            df['Order_month']=df['Order_Date'].dt.month
            df['Order_year']=df['Order_Date'].dt.year
            
            df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'])

            # Creating two new column for hour and minute
            df['Hour_order']=df['Time_Orderd'].dt.hour
            df['Min_order']=df['Time_Orderd'].dt.minute
            
            df.drop(["Time_Orderd", "Order_Date"],axis = 1, inplace= True)
            
            df = self.create_delivery_features(df)
            
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()