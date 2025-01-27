from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
from src.pipeline.prediction import PredictPipeline
from src.utils.logger import logging
from src.utils.utils import (get_traffic_density, get_traffic_index, get_coordinates, get_weather, data_into_db,get_db_connection)

app = Flask(__name__)
CORS(app)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = {
        'totalDeliveries': 2154,
        'averageTime': 25,
        'vehicleUtilization': 90,
        'totalCost': 150.75
    }
    return jsonify(metrics)

@app.route('/trendData', methods=['GET'])
def get_trend_data():
    trend_data = [
        {
            'timestamp': datetime(2024, 1, 1, i).isoformat(),  # Changed month from 0 to 1
            'deliveryTime': 20 + (i % 5),
            'traffic': 40 + (i % 10),
            'temperature': 15 + (i % 3)
        }
        for i in range(24)
    ]
    return jsonify(trend_data)

@app.route('/predict', methods=['POST'])
def predict_delivery_time():
    try:
        data = request.json
        logging.info(f"Received data from frontend (predict): {data}")
        
        global delivery_location_latitude, delivery_location_longitude,pickup_location_latitude, pickup_location_longitude

        # pickup_location_latitude, pickup_location_longitude,City = get_coordinates(data['pickupAddress'])
        # logging.info(f"pickup_location: {pickup_location_latitude}, {pickup_location_longitude}")
        # delivery_location_latitude, delivery_location_longitude,city = get_coordinates(data['address'])
        # logging.info(f"delivery_location: {delivery_location_latitude}, {delivery_location_longitude}")
        
        # temperature,weathercondition = get_weather(City)
        
        # if data['city'] == "Metropolitan":
        #     data['city'] = "Metropolitian"
        # else:
        #     None
            
        
        # if not pickup_location_latitude or not pickup_location_longitude or not delivery_location_latitude or not delivery_location_longitude:
        #     return jsonify({'error': 'Invalid address'}), 400
        
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
        now = datetime.now()
        
        traffic_index = get_traffic_index(latitude=delivery_location_latitude, longitude=delivery_location_longitude)
        
        pipeline_params = {
            'ID': int(uuid.uuid4().hex[:4], 16),
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
        data = request.json
        print("Received data from frontend (geocode):", data)
        
        global latitude, longitude
        
        address = data['address']
        latitude, longitude = delivery_location_latitude, delivery_location_longitude
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

<<<<<<< HEAD
<<<<<<< HEAD
@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM deliveries")
        total_deliveries = cursor.fetchone()[0]

        cursor.execute("SELECT Time_taken FROM deliveries")
        delivery_times = [row[0] for row in cursor.fetchall()]
        avg_time = round(mean(delivery_times), 2) if delivery_times else 0

        cursor.execute("""
            SELECT COUNT(DISTINCT vehicle_id) 
            FROM deliveries 
            WHERE DATE(order_date) = CURRENT_DATE
        """)
        active_vehicles = cursor.fetchone()[0]
        total_vehicles = 100
        utilization = round((active_vehicles / total_vehicles) * 100, 2)

        metrics = {
            'totalDeliveries': total_deliveries,
            'averageTime': avg_time,
            'vehicleUtilization': utilization
        }

        conn.close()
        return jsonify(metrics)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/trendData', methods=['GET'])
def get_trend_data():
    try:
        trend_data = [
            {
                'timestamp': datetime(2024, 1, 1, i).isoformat(),
                'deliveryTime': 20 + (i % 5),
                'traffic': 40 + (i % 10),
                'temperature': 15 + (i % 3)
            }
            for i in range(24)
        ]
        return jsonify(trend_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
=======
>>>>>>> parent of 4791ba1 (metrics, delivery trend and prediction is working just fine)
=======
>>>>>>> parent of 4791ba1 (metrics, delivery trend and prediction is working just fine)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Server is running in http://localhost:5000")