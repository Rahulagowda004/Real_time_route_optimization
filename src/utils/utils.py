import os
import sys
import time
import pickle
import requests
import numpy as np 
import pandas as pd   
import mysql.connector
from dotenv import load_dotenv
from sklearn.metrics import r2_score
from opencage.geocoder import OpenCageGeocode
from src.utils.exception import CustomException
from src.utils.logger import logging
from sklearn.model_selection import GridSearchCV

load_dotenv()

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}
        for model_name, model in models.items():
            print(f"Training {model_name}...")
            start_time = time.time()

            # Apply GridSearchCV if hyperparameters are provided
            if param.get(model_name):
                gs = GridSearchCV(model, param[model_name], cv=3, n_jobs=-1, verbose=1)
                gs.fit(X_train, y_train)
                model = gs.best_estimator_
            else:
                model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            print(f"{model_name} completed in {time.time() - start_time:.2f} seconds.")

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    


def get_coordinates(address):
    try:
        geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
        result = geocoder.geocode(address)
        if result:
            geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
            result = geocoder.geocode(address)
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            city = result[0]['components'].get('city') or \
                result[0]['components'].get('town') or \
                result[0]['components'].get('village')
            return lat, lng, city
        else:
            logging.info("Address not found")
            print("Address not found")
            return None, None, None
    except Exception as e:
        logging.error(CustomException(e, sys))
        raise CustomException(e, sys)
    
def get_traffic_index( latitude, longitude):
    try:
        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        params = {
            'key': os.getenv("TOMTOM_API_KEY"),
            'point': f"{latitude},{longitude}"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                flow_data = data['flowSegmentData']
                current_travel_time = flow_data['currentTravelTime']
                free_flow_travel_time = flow_data['freeFlowTravelTime']
                
                traffic_index = current_travel_time / free_flow_travel_time
                return float(traffic_index)
            except KeyError:
                print("KeyError: Required data missing in response.")
                return 2.0
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return 2.0
    except Exception as e:      
        raise CustomException(e, sys)

def get_traffic_density(traffic_index):
    if traffic_index <= 1.0:
        return "Low"
    elif 1.1 <= traffic_index <= 2.0:
        return "Medium"
    elif 2.1 <= traffic_index <= 3.0:
        return "High"
    else:
        return "Jam"
    
def get_weather(city):
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract temperature in Kelvin and convert to Celsius
            temperature_kelvin = data['main']['temp']
            Temperature = temperature_kelvin - 273.15

            # Map weather condition codes to conditions
            weather_mapping = {
                "Clear": "Sunny",
                "Thunderstorm": "Stormy",
                "Dust": "Sandstorms",
                "Haze": "Sandstorms",
                "Clouds": "Cloudy",
                "Mist": "Fog",
                "Fog": "Fog",
                "Smoke": "Fog",
                "Drizzle": "Cloudy",
                "Rain": "Cloudy",
                "Squall": "Windy",
                "Tornado": "Windy",
                "Ash": "Sandstorms",
                "Sand": "Sandstorms",
            }

            # Extract main weather description
            weather_main = data['weather'][0]['main']

            # Get mapped condition or fallback to default
            weathercondition = weather_mapping.get(weather_main, weather_main)
            logging.info("Weather data fetched successfully")
            return Temperature, weathercondition
        else:
            logging.info("Error fetching weather data")
            response.raise_for_status()
    except Exception as e:   
        raise CustomException(e, sys)
    
def get_db_connection():

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def data_into_db(data):
    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO raw_data (
            ID, Delivery_person_Age, Delivery_person_Ratings, pickup_location_latitude, pickup_location_longitude,
            Delivery_location_latitude, Delivery_location_longitude, Order_Date, Time_Orderd, 
            Weatherconditions, Road_traffic_density, Vehicle_condition, Type_of_vehicle, 
            multiple_deliveries, City, Temperature, Traffic_Index, Time_taken
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            data['ID'], data['delivery_person_age'], data['delivery_person_ratings'],  # Adjusted here
            data['translogi_latitude'], data['translogi_longitude'], data['delivery_location_latitude'], 
            data['delivery_location_longitude'], data['order_date'], data['time_orderd'], 
            data['weatherconditions'], data['road_traffic_density'], data['vehicle_condition'], 
            data['type_of_vehicle'], data['multiple_deliveries'], data['city'], 
            data['temperature'], data['traffic_index'], data['Time_taken']
        ))

        connection.commit()
        logging.info("Data inserted successfully into raw_data table")
    except Exception as e:
        logging.error(CustomException(e, sys))
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def routes_to_db(route_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Convert instructions list to string
        instructions_str = '\n'.join(
            f"{i+1}. {instruction}" 
            for i, instruction in enumerate(route_data['instructions'])
        )

        insert_query = """
        INSERT INTO optimized_routes (
            pickup_lat, pickup_lng, delivery_lat, delivery_lng,
            total_distance, instructions
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            route_data['pickup_lat'],
            route_data['pickup_lng'], 
            route_data['delivery_lat'],
            route_data['delivery_lng'],
            route_data['total_distance'],
            instructions_str
        )

        cursor.execute(insert_query, values)
        connection.commit()
        logging.info("Route data inserted successfully into optimized_routes table")
    except Exception as e:
        logging.error(CustomException(e, sys))
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()