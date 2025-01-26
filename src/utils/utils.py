import os
import sys
import time
import pickle
import requests
import numpy as np 
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.utils.exception import CustomException
from opencage.geocoder import OpenCageGeocode

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
    
geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))

def get_coordinates(address):
    result = geocoder.geocode(address)
    
    if result:
        city = result[0]['components']['_normalized_city']
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        print(f"Latitude: {lat}, Longitude: {lng}")
        return lat, lng, city
    else:
        print("Address not found")
        return None, None, None
    
def get_traffic_index( latitude, longitude):
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

        return Temperature, weathercondition
    else:
        response.raise_for_status()