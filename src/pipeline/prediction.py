import sys
import os
import joblib
import pandas as pd
from geopy.distance import geodesic
from src.utils.exception import CustomException
from src.utils.utils import load_object

import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)


class Preprocess:
    def __init__(self):
        try:
            self.avg_delivery_time_area = joblib.load('artifacts/preprocessor/avg_delivery_time_area.pkl')
            self.traffic_weather_impact = joblib.load('artifacts/preprocessor/traffic_weather_impact.pkl')
            self.max_deliveries_per_vehicle = joblib.load('artifacts/preprocessor/max_deliveries_per_vehicle.pkl')
        except Exception as e:
            raise CustomException(e, sys)
    
    def clean_df(self, df):
        df = df.copy()
        try:
            def add_features_for_prediction(df):
                try:
                    df['avg_delivery_time_area'] = df['City'].map(self.avg_delivery_time_area)
                    
                    df['traffic_weather_impact'] = df.apply(
                        lambda row: self.traffic_weather_impact.get((row['Road_traffic_density'], row['Weatherconditions']), None),
                        axis=1
                    )
                    
                    df['vehicle_capacity_utilization'] = df.apply(
                        lambda row: row['multiple_deliveries'] / self.max_deliveries_per_vehicle.get(row['Type_of_vehicle'], 1),
                        axis=1
                    ).fillna(0)
                    
                    def calculate_distance(row):
                        restaurant_coords = (row['translogi_latitude'], row['translogi_longitude'])
                        delivery_coords = (row['Delivery_location_latitude'], row['Delivery_location_longitude'])
                        return geodesic(restaurant_coords, delivery_coords).kilometers
                    
                    df['distance'] = df.apply(calculate_distance, axis=1)
                    return df
                except Exception as e:
                    raise CustomException(e, sys)
            
            df.drop(['ID'], axis=1, inplace=True)
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
            df['Order_day'] = df['Order_Date'].dt.day
            df['Order_month'] = df['Order_Date'].dt.month
            df['Order_year'] = df['Order_Date'].dt.year
            df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'])
            df['Hour_order']=df['Time_Orderd'].dt.hour
            df['Min_order']=df['Time_Orderd'].dt.minute
            df.drop(["Time_Orderd", "Order_Date"],axis = 1, inplace= True)
            df['city'] = df['City'].fillna("unknown",inplace=True)
            df = add_features_for_prediction(df)
            return df
        except Exception as e:
            raise CustomException(e,sys)

class PredictPipeline:
    def __init__(self):
        try:
            self.model_path = os.path.join("artifacts/model", "best_model.pkl")
            self.preprocessor_path = os.path.join("artifacts/preprocessor", "preprocessor.pkl")
            self.model = load_object(self.model_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self, dataframe):
        try:
            preprocess = Preprocess()
            dataframe = preprocess.clean_df(dataframe)
            preprocessor = joblib.load(self.preprocessor_path)
            data_scaled = preprocessor.transform(dataframe)
            predicted_time = self.model.predict(data_scaled)
            return predicted_time
        except Exception as e:
            raise CustomException(e, sys)
        
# if __name__ == "__main__":
#     try:
#         pipeline = PredictPipeline()
#         df = pd.read_csv("artifacts/prediction/prediction.csv")
#         Time_taken = pipeline.predict(df)
#         print(Time_taken)
#     except Exception as e:
#         print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Define the input data as a dictionary
        input_data = {
            "ID": ["0x4607"],
            "Delivery_person_Age": [37.0],
            "Delivery_person_Ratings": [4.9],
            "translogi_latitude": [22.745049],
            "translogi_longitude": [75.892471],
            "Delivery_location_latitude": [22.765049],
            "Delivery_location_longitude": [75.912471],
            "Order_Date": ["2022-03-19"],
            "Time_Orderd": ["11:30:00"],
            "Road_traffic_density": ["High"],
            "Weatherconditions": ["Sunny"],
            "Vehicle_condition": [2],
            "Type_of_vehicle": ["motorcycle"],
            "multiple_deliveries": [0.0],
            "City": ["Urban"],
            "Temperature": [29.0],
            "Traffic_Index": [1.2]
        }

        input_df = pd.DataFrame(input_data)
        pipeline = PredictPipeline()
        predicted_time = pipeline.predict(input_df)
        print(f"Predicted Time Taken: {predicted_time}")
    except Exception as e:
        print(f"An error occurred: {e}")