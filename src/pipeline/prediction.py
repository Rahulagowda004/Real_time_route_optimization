import sys
import os
import pandas as pd
from src.utils.exception import CustomException
from src.utils.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
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