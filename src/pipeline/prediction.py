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
        
    def get_data_transformer_object(self):
        try:
            # Numerical features including time components
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

class PredictPipeline:
    def __init__(self):
        try:
            self.model_path = os.path.join("artifacts/model", "best_model.pkl")
            self.model = load_object(self.model_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self, dataframe):
        try:
            preprocess = Preprocess()
            dataframe = preprocess.clean_df(dataframe)
            preprocessor = preprocess.get_data_transformer_object()
            data_scaled = preprocessor.fit_transform(dataframe)
            preds = self.model.predict(data_scaled)
            print("Predictions: ", preds)
            preds_df = pd.DataFrame(preds, columns=['Predictions'])
            return preds_df
        except Exception as e:
            raise CustomException(e, sys)

class CustomClass:
    def __init__(
        self,
        ID: int,
        delivery_person_age: float,
        delivery_person_ratings: float,
        translogi_latitude: float,
        translogi_longitude: float,
        delivery_location_latitude: float,
        delivery_location_longitude: float,
        order_date: str,  # Assuming 'Order_Date' is a string or datetime object
        time_orderd: float,  # Assuming 'Time_Orderd' is float type representing the time
        weatherconditions: str,
        road_traffic_density: str,
        vehicle_condition: int,
        type_of_vehicle: str,
        multiple_deliveries: float,
        city: str,
        temperature: float,  # Added temperature as per the new list
        traffic_index: float,  # Added traffic index as per the new list
        time_taken: float  # Replaced avg_delivery_time_area with Time_taken
    ):
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
        self.time_taken = time_taken

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "ID": [self.ID],
                "Delivery_person_Age": [self.delivery_person_age],
                "Delivery_person_Ratings": [self.delivery_person_ratings],
                "translogi_latitude": [self.translogi_latitude],
                "translogi_longitude": [self.translogi_longitude],
                "Delivery_location_latitude": [self.delivery_location_latitude],
                "Delivery_location_longitude": [self.delivery_location_longitude],
                "Order_Date": [self.order_date],
                "Time_Orderd": [self.time_orderd],
                "Weatherconditions": [self.weatherconditions],
                "Road_traffic_density": [self.road_traffic_density],
                "Vehicle_condition": [self.vehicle_condition],
                "Type_of_vehicle": [self.type_of_vehicle],
                "multiple_deliveries": [self.multiple_deliveries],
                "City": [self.city],
                "Temperature": [self.temperature],
                "Traffic_Index": [self.traffic_index],
                "Time_taken": [self.time_taken]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
    
    def custom_predicton(self):
        try:
            data = self.get_data_as_data_frame()
            pipeline = PredictPipeline()
            predictions = pipeline.predict(data)
            return predictions
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        pipeline = PredictPipeline()
        df = pd.read_csv("artifacts/Data/dataset.csv")
        predictions = pipeline.predict(df)
        print(predictions)
    except Exception as e:
        print(f"An error occurred: {e}")