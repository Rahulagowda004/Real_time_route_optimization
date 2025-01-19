import sys
import os
import joblib
import pandas as pd
from geopy.distance import geodesic
from src.utils.exception import CustomException
from src.utils.utils import load_object

class preprocess:
    def __init__(self):
        # Load pre-trained preprocessor objects
        self.avg_delivery_time_area = joblib.load('artifacts/preprocessor/avg_delivery_time_area.pkl')
        self.traffic_weather_impact = joblib.load('artifacts/preprocessor/traffic_weather_impact.pkl')
        self.max_deliveries_per_vehicle = joblib.load('artifacts/preprocessor/max_deliveries_per_vehicle.pkl')

    
    def clean_df(self,df):
        
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
                    raise CustomException(e,sys)
            
            df.drop(['ID'], axis=1, inplace=True) #dropping the ID column(irrelavant)
            df['Order_Date']=pd.to_datetime(df['Order_Date'])
            df['Order_day']=df['Order_Date'].dt.day
            df['Order_month']=df['Order_Date'].dt.month
            df['Order_year']=df['Order_Date'].dt.year
            df['Time_Orderd'] = pd.to_datetime(df['Time_Orderd'])
            df['Hour_order']=df['Time_Orderd'].dt.hour
            df['Min_order']=df['Time_Orderd'].dt.minute
            df.drop(["Time_Orderd", "Order_Date"],axis = 1, inplace= True)  
            df = add_features_for_prediction(df)
            return df
        except Exception as e:
            raise CustomException(e,sys)

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,dataframe):
        try:
            model_path=os.path.join("artifacts/model","best_model.pkl")
            preprocessor_path=os.path.join('artifacts/preprocessor','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            
            clean = preprocess()
            dataframe=clean.clean_df(dataframe)
            
            data_scaled=preprocessor.transform(dataframe)
            preds=model.predict(data_scaled)
            print("Predictions: ",preds)
            preds = pd.DataFrame(preds, columns=['Predictions'])
            preds.to_csv("artifacts/Prediction/Predictions.csv", index=False)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(
        self,
        delivery_person_age: float,
        delivery_person_ratings: float,
        delivery_location_latitude: float,
        delivery_location_longitude: float,
        weatherconditions: str,
        road_traffic_density: str,
        vehicle_condition: int,
        type_of_vehicle: str,
        multiple_deliveries: float,
        city: str,
        order_day: int,
        order_month: int,
        order_year: int,
        hour_order: float,
        min_order: float,
        avg_delivery_time_area: float,
        traffic_weather_impact: float,
        vehicle_capacity_utilization: float
    ):
        self.delivery_person_age = delivery_person_age
        self.delivery_person_ratings = delivery_person_ratings
        self.delivery_location_latitude = delivery_location_latitude
        self.delivery_location_longitude = delivery_location_longitude
        self.weatherconditions = weatherconditions
        self.road_traffic_density = road_traffic_density
        self.vehicle_condition = vehicle_condition
        self.type_of_vehicle = type_of_vehicle
        self.multiple_deliveries = multiple_deliveries
        self.city = city
        self.order_day = order_day
        self.order_month = order_month
        self.order_year = order_year
        self.hour_order = hour_order
        self.min_order = min_order
        self.avg_delivery_time_area = avg_delivery_time_area
        self.traffic_weather_impact = traffic_weather_impact
        self.vehicle_capacity_utilization = vehicle_capacity_utilization

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "Delivery_person_Age": [self.delivery_person_age],
                "Delivery_person_Ratings": [self.delivery_person_ratings],
                "Delivery_location_latitude": [self.delivery_location_latitude],
                "Delivery_location_longitude": [self.delivery_location_longitude],
                "Weatherconditions": [self.weatherconditions],
                "Road_traffic_density": [self.road_traffic_density],
                "Vehicle_condition": [self.vehicle_condition],
                "Type_of_vehicle": [self.type_of_vehicle],
                "multiple_deliveries": [self.multiple_deliveries],
                "City": [self.city],
                "Order_day": [self.order_day],
                "Order_month": [self.order_month],
                "Order_year": [self.order_year],
                "Hour_order": [self.hour_order],
                "Min_order": [self.min_order],
                "avg_delivery_time_area": [self.avg_delivery_time_area],
                "traffic_weather_impact": [self.traffic_weather_impact],
                "vehicle_capacity_utilization": [self.vehicle_capacity_utilization]
            }
            
            
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
        
    # df = self.get_data_as_data_frame()
    # obj = PredictPipeline()
    # time_taken = obj.predict(df)
    # print("The time consuming for the delivery would be: ", time_taken)
        
if __name__ == "__main__":
    obj=PredictPipeline()
    df = pd.read_csv("artifacts/Prediction/test.csv")
    obj.predict(df)