import uuid
from flask_cors import CORS
from datetime import datetime
from src.utils.logger import logging
from flask import Flask, request, jsonify
from src.pipeline.prediction import PredictPipeline
from src.utils.utils import (get_traffic_density, get_traffic_index,get_coordinates,get_weather,data_into_db)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict_delivery_time():
    try:
        data = request.json
        logging.info(f"Received data from frontend (predict): {data}")

        pickup_location_latitude, pickup_location_longitude,City = get_coordinates(data['pickupAddress'])
        logging.info(f"pickup_location: {pickup_location_latitude}, {pickup_location_longitude}")
        delivery_location_latitude, delivery_location_longitude,city = get_coordinates(data['address'])
        logging.info(f"delivery_location: {delivery_location_latitude}, {delivery_location_longitude}")
        
        temperature,weathercondition = get_weather(City)
        
        if not pickup_location_latitude or not pickup_location_longitude or not delivery_location_latitude or not delivery_location_longitude:
            return jsonify({'error': 'Invalid address'}), 400

        now = datetime.now()
        
        traffic_index = get_traffic_index(latitude=delivery_location_latitude, longitude=delivery_location_longitude)
        
        data_dict = {
            "ID": str(uuid.uuid4()),
            "delivery_person_age": 37.0,
            "delivery_person_ratings": 4.9,
            "translogi_latitude": pickup_location_latitude,
            "translogi_longitude": pickup_location_longitude,
            "delivery_location_latitude": delivery_location_latitude,
            "delivery_location_longitude": delivery_location_longitude,
            "order_date": now.strftime("%d-%m-%y"),
            "time_orderd": now.strftime("%H:%M:%S"),
            "road_traffic_density": get_traffic_density(traffic_index),
            "weatherconditions": weathercondition,
            "vehicle_condition": 2,
            "type_of_vehicle": "motorcycle",
            "multiple_deliveries": 0.0,
            "city": data['city'],
            "temperature": temperature,
            "traffic_index": traffic_index
        }
        
        # pipeline = PredictPipeline(**data)
        pipeline = PredictPipeline(
            ID=data_dict["ID"],
            delivery_person_age=data_dict["delivery_person_age"],
            delivery_person_ratings=data_dict["delivery_person_ratings"],
            translogi_latitude=data_dict["translogi_latitude"],
            translogi_longitude=data_dict["translogi_longitude"],
            delivery_location_latitude=data_dict["delivery_location_latitude"],
            delivery_location_longitude=data_dict["delivery_location_longitude"],
            order_date=data_dict["order_date"],
            time_orderd=data_dict["time_orderd"],
            road_traffic_density=data_dict["traffic_index"],
            weatherconditions=data_dict["weatherconditions"],
            vehicle_condition=data_dict["vehicle_condition"],
            type_of_vehicle=data_dict["type_of_vehicle"],
            multiple_deliveries=data_dict["multiple_deliveries"],
            city=data_dict["city"],
            temperature=data_dict["temperature"],
            traffic_index=data_dict["traffic_index"]
        )
        
        logging.info(f"pipeline: {pipeline}")
        predicted_time = pipeline.predict()
        data['Time_taken'] = predicted_time
        data_into_db(data)
        logging.info(f"predicted_time: {predicted_time}")
        return jsonify({
            'predicted_time': predicted_time.astype(float)
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
        latitude, longitude,city = get_coordinates(address)
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