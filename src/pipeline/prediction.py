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
    def __init__(self,
                ID: str,
                delivery_person_age: float,
                delivery_person_ratings: float,
                translogi_latitude: float,
                translogi_longitude: float,
                delivery_location_latitude: float,
                delivery_location_longitude: float,
                order_date: str,
                time_orderd: str,
                weatherconditions: str,
                road_traffic_density: str,
                vehicle_condition: int,
                type_of_vehicle: str,
                multiple_deliveries: float,
                city: str,
                temperature: float,
                traffic_index: float
                ):
        try:
            self.ID = ID
            self.delivery_person_age = delivery_person_age
            self.delivery_person_ratings = delivery_person_ratings
            self.translogi_latitude = translogi_latitude
            self.translogi_longitude = translogi_longitude
            self.delivery_location_latitude = delivery_location_latitude
            self.delivery_location_longitude = delivery_location_longitude
            self.order_date = order_date
            self.time_orderd = time_orderd
            self.weatherconditions = weatherconditions
            self.road_traffic_density = road_traffic_density
            self.vehicle_condition = vehicle_condition
            self.type_of_vehicle = type_of_vehicle
            self.multiple_deliveries = multiple_deliveries
            self.city = city
            self.temperature = temperature
            self.traffic_index = traffic_index
            self.model_path = os.path.join("artifacts/model", "best_model.pkl")
            self.preprocessor_path = os.path.join("artifacts/preprocessor", "preprocessor.pkl")
            self.model = load_object(self.model_path)
            self.preprocessor = load_object(self.preprocessor_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'ID': [self.ID],
                'Delivery_person_Age': [self.delivery_person_age],
                'Delivery_person_Ratings': [self.delivery_person_ratings],
                'translogi_latitude': [self.translogi_latitude],
                'translogi_longitude': [self.translogi_longitude],
                'Delivery_location_latitude': [self.delivery_location_latitude],
                'Delivery_location_longitude': [self.delivery_location_longitude],
                'Order_Date': [self.order_date],
                'Time_Orderd': [self.time_orderd],
                'Weatherconditions': [self.weatherconditions],
                'Road_traffic_density': [self.road_traffic_density],
                'Vehicle_condition': [self.vehicle_condition],
                'Type_of_vehicle': [self.type_of_vehicle],
                'multiple_deliveries': [self.multiple_deliveries],
                'City': [self.city],
                'Temperature': [self.temperature],
                'Traffic_Index': [self.traffic_index]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self):
        try:
            preprocess = Preprocess()
            dataframe = self.get_data_as_dataframe()
            dataframe = preprocess.clean_df(dataframe)
            data_scaled = self.preprocessor.transform(dataframe)
            predicted_time = self.model.predict(data_scaled)
            return predicted_time
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    try:
        pipeline = PredictPipeline(
            ID="0x4607",
            delivery_person_age=37.0,
            delivery_person_ratings=4.9,
            translogi_latitude=22.745049,
            translogi_longitude=75.892471,
            delivery_location_latitude=22.765049,
            delivery_location_longitude=75.912471,
            order_date="2022-03-19",
            time_orderd="11:30:00",
            road_traffic_density="High",
            weatherconditions="Sunny",
            vehicle_condition=2,
            type_of_vehicle="motorcycle",
            multiple_deliveries=0.0,
            city="Urban",
            temperature=29.0,
            traffic_index=1.2
        )
        print(pipeline.predict())
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