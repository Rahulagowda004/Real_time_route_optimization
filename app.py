from flask_cors import CORS
from datetime import datetime
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
from src.pipeline.prediction import PredictPipeline
from src.utils.utils import (get_temperature,get_weatherconditions,get_traffic_density,get_traffic_index)

app = Flask(__name__)
CORS(app)

geolocator = Nominatim(user_agent="delivery_app")

@app.route('/predict', methods=['POST'])
def predict_delivery_time():
    try:
        data = request.json
        
        # Geocode pickup and delivery addresses
        pickup_location = geolocator.geocode(data['pickupAddress'])
        delivery_location = geolocator.geocode(data['address'])
        
        if not pickup_location or not delivery_location:
            return jsonify({'error': 'Invalid address'}), 400

        # Current date and time
        now = datetime.now()
        
        traffic_index = get_traffic_index(latitude=delivery_location.latitude, longitude=delivery_location.longitude)
        pipeline = PredictPipeline(
            ID="0x4607",
            delivery_person_age=37.0,
            delivery_person_ratings=4.9,
            translogi_latitude=pickup_location.latitude,
            translogi_longitude=pickup_location.longitude,
            delivery_location_latitude=delivery_location.latitude,
            delivery_location_longitude=delivery_location.longitude,
            order_date=now.strftime("%d-%m-%y"),
            time_orderd=now.strftime("%H:%M:%S"),
            road_traffic_density=get_traffic_density(traffic_index),
            weatherconditions=get_weatherconditions(latitude=delivery_location.latitude, longitude=delivery_location.longitude),
            vehicle_condition=2,
            type_of_vehicle="motorcycle",
            multiple_deliveries=0.0,
            city="Urban",
            temperature=get_temperature(latitude=delivery_location.latitude, longitude=delivery_location.longitude),
            traffic_index=traffic_index
            )
        predicted_time = pipeline.predict()
        return jsonify({
            'predicted_time': round(float(predicted_time), 2)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
        
@app.route('/geocode', methods=['POST'])
def geocode_address():
    try:
        data = request.json
        address = data['address']
        
        location = geolocator.geocode(address)
        if location:
            return jsonify({
                'lat': location.latitude,
                'lng': location.longitude
            })
        else:
            return jsonify({'error': 'Address not found'}), 404
            
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)