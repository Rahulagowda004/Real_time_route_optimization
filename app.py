from flask_cors import CORS
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from src.pipeline.prediction import PredictPipeline
from src.utils.logger import logging
import mysql
from src.utils.utils import (get_traffic_density, get_traffic_index,get_coordinates,get_weather,get_db_connection)

app = Flask(__name__)
CORS(app)

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
        print("Record inserted successfully!")

    except mysql.connector.Error as e:
        print(f"Error inserting data into MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")


@app.route('/predict', methods=['POST'])
def predict_delivery_time():
    try:
        data = request.json
        # logging.info(f"Received data from frontend (predict): {data}")

        # pickup_location_latitude, pickup_location_longitude,City = get_coordinates(data['pickupAddress'])
        # logging.info(f"pickup_location: {pickup_location_latitude}, {pickup_location_longitude}")
        # delivery_location_latitude, delivery_location_longitude,city = get_coordinates(data['address'])
        # logging.info(f"delivery_location: {delivery_location_latitude}, {delivery_location_longitude}")
        
        # temperature,weathercondition = get_weather(City)
        
        # if not pickup_location_latitude or not pickup_location_longitude or not delivery_location_latitude or not delivery_location_longitude:
        #     return jsonify({'error': 'Invalid address'}), 400

        # now = datetime.now()
        
        # traffic_index = get_traffic_index(latitude=delivery_location_latitude, longitude=delivery_location_longitude)
        global delivery_location_latitude, delivery_location_longitude, city
        city = "banlgore"
        ID = int(uuid.uuid4().hex[:4], 16)
        pickup_location_latitude = 22.745049
        pickup_location_longitude = 75.892471
        delivery_location_latitude = 22.765049
        delivery_location_longitude = 75.912471
        traffic_index = 1.2
        weathercondition = "Sunny"
        temperature = 29.0
        now = datetime.now()
        data = {
            "city": "Urban"
        }
        logging.info(f"""ID: {ID},
                pickup_location_latitude: {pickup_location_latitude},
                pickup_location_longitude: {pickup_location_longitude},
                delivery_location_latitude: {delivery_location_latitude},
                delivery_location_longitude: {delivery_location_longitude},
                order_date: {now.strftime('%d-%m-%y')},
                time_orderd: {now.strftime('%H:%M:%S')},
                road_traffic_density: {get_traffic_density(traffic_index)},
                weatherconditions: {weathercondition},
                city: {data['city']}, temperature: {temperature},
                traffic_index: {traffic_index}""")
        
        pipeline_params = {
            'ID': ID,
            'delivery_person_age': 37.0,
            'delivery_person_ratings': 4.9,
            'translogi_latitude': pickup_location_latitude,
            'translogi_longitude': pickup_location_longitude,
            'delivery_location_latitude': delivery_location_latitude,
            'delivery_location_longitude': delivery_location_longitude,
            'order_date': now.strftime("%d-%m-%y"),
            'time_orderd': now.strftime("%H:%M:%S"),
            'road_traffic_density': get_traffic_density(traffic_index),
            'weatherconditions': weathercondition,
            'vehicle_condition': 2,
            'type_of_vehicle': "motorcycle",
            'multiple_deliveries': 0.0,
            'city': data['city'],
            'temperature': temperature,
            'traffic_index': traffic_index
        }
        logging.info(f"pipeline_params: {pipeline_params}")
        pipeline = PredictPipeline(**pipeline_params)
        logging.info(f"pipeline: {pipeline}")
        predicted_time = pipeline.predict()
        logging.info(f"predicted_time: {predicted_time}")
        pipeline_params['Time_taken'] = predicted_time[0]
        data_into_db(pipeline_params)
        return jsonify({
            'predicted_time': round(predicted_time[0], 2)
        })
    
    except Exception as e:
        print("Error in /predict:", str(e))
        return jsonify({
            'error': str(e)
        }), 500
        
@app.route('/geocode', methods=['POST'])
def geocode_address():
    try:
        # Log the received data
        data = request.json
        print("Received data from frontend (geocode):", data)
        
        address = data['address']
        # latitude, longitude,city = get_coordinates(address)
        latitude, longitude,city = delivery_location_latitude, delivery_location_longitude, city
        logging.info(f"geoadress latitude: {latitude}, longitude: {longitude}")
        if latitude and longitude:
            return jsonify({
                'lat': latitude,
                'lng': longitude
            })
        else:
            return jsonify({'error': 'Address not found'}), 404
            
    except Exception as e:
        print("Error in /geocode:", str(e))
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Server is running in http://localhost:5000")