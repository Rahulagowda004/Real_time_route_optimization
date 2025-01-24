import sys
import os
import joblib
import pandas as pd
from geopy.distance import geodesic
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, RobustScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from src.utils.exception import CustomException
from src.utils.utils import load_object

import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)


class Preprocess:
    def __init__(self):
        # Load pre-trained preprocessor objects
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
            
            df.drop(['ID'], axis=1, inplace=True)  # Drop irrelevant column
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
            self.model = load_object(self.model_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self, dataframe):
        try:
            preprocessor = self.get_data_transformer_object()

            preprocess = Preprocess()
            dataframe = preprocess.clean_df(dataframe)
            
            data_scaled = preprocessor.fit_transform(dataframe)
            preds = self.model.predict(data_scaled)
            print("Predictions: ", preds)

            preds_df = pd.DataFrame(preds, columns=['Predictions'])
            preds_df.to_csv("artifacts/Prediction/Predictions.csv", index=False)
            return preds_df
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformer_object(self):
        try:
            # Numerical features including time components
            mean_features = [
                "Delivery_person_Age",
                "Delivery_person_Ratings",
                "avg_delivery_time_area",
                "vehicle_capacity_utilization",
                "Order_day",
                "Order_month",
                "Order_year",
                "Hour_order",
                "Min_order",
                "distance",
            ]
            
            location_features = [
                "translogi_latitude",
                "translogi_longitude",
                "Delivery_location_latitude",
                "Delivery_location_longitude",
                "distance"
            ]
            
            # Only truly categorical features
            mode_features = [
                "multiple_deliveries",
                "traffic_weather_impact"
            ]
            
            cat_features = [
                "Weatherconditions",
                "Road_traffic_density",
                "City",
                "Type_of_vehicle"
            ]
            
            ordinal_features = ["Vehicle_condition"]

            mean_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", RobustScaler())
                ]
            )

            mode_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(drop='first', sparse_output=False, handle_unknown="ignore"))
                ]
            )

            ordinal_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ordinal", OrdinalEncoder())
                ]
            )
            
            location_pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler())
                ]
            )
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", mean_pipeline, mean_features),
                    ("cat_pipeline", mode_pipeline, cat_features),
                    ("mode_pipeline", mode_pipeline, mode_features),
                    ("ordinal_pipeline", ordinal_pipeline, ordinal_features),
                    ("location_pipeline", location_pipeline, location_features)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)


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


if __name__ == "__main__":
    try:
        pipeline = PredictPipeline()
        df = pd.read_csv("artifacts/Prediction/Validation_set.csv")
        predictions = pipeline.predict(df)
        print(predictions)
    except Exception as e:
        print(f"An error occurred: {e}")