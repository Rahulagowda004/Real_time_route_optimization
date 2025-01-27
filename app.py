from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
from src.pipeline.prediction import PredictPipeline
from src.utils.logger import logging
from src.utils.utils import (get_traffic_density, get_traffic_index, get_coordinates, get_weather, data_into_db,get_db_connection,routes_to_db)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict_delivery_time():
    try:
        data = request.json
        logging.info(f"Received data from frontend: {data}")
        
        pickup_location_latitude, pickup_location_longitude,City = get_coordinates(data['pickupAddress'])
        logging.info(f"pickup_location: {pickup_location_latitude}, {pickup_location_longitude}")
        delivery_location_latitude, delivery_location_longitude,city = get_coordinates(data['address'])
        logging.info(f"delivery_location: {delivery_location_latitude}, {delivery_location_longitude}")
        
        temperature,weathercondition = get_weather(City)
        
        if data['city'] == "Metropolitan":
            data['city'] = "Metropolitian"
        else:
            None
            
        
        if not pickup_location_latitude or not pickup_location_longitude or not delivery_location_latitude or not delivery_location_longitude:
            return jsonify({'error': 'Invalid address'}), 400
        
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

        response_data = {
            'predicted_time': round(predicted_time[0], 2),
            'pickup': {
                'lat': float(pickup_location_latitude),
                'lng': float(pickup_location_longitude)
            },
            'delivery': {
                'lat': float(delivery_location_latitude),
                'lng': float(delivery_location_longitude)
            }
        }
        
        logging.info(f"Sending response: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"Error in predict_delivery_time: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
                'temperature': 155 + (i % 3)
            }
            for i in range(24)
        ]
        return jsonify(trend_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/route-directions', methods=['POST'])
def save_route_directions():
    try:
        data = request.json
        logging.info(f"Received route directions: {data}")

        pickup = data['pickup']
        delivery = data['delivery']
        directions = data['directions']
        
        route_data = {
            'pickup_lat': pickup['lat'],
            'pickup_lng': pickup['lng'],
            'delivery_lat': delivery['lat'],
            'delivery_lng': delivery['lng'],
            'total_distance': directions['distance'],
            'instructions': directions['instructions']
        }

        logging.info(f"Saving route data to database: {route_data}")
        
        routes_to_db(route_data)
        
        logging.info("Route directions saved successfully!")
        
        print("Everything completed successfully")
        
        return jsonify({
            'message': 'Route directions received successfully',
            'route': route_data
        })
    
    except Exception as e:
        logging.error(f"Error processing route directions: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print("Server is running in http://localhost:5000")