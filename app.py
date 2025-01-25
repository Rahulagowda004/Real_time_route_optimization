from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from catboost import CatBoostRegressor
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

# Load the pre-trained model
model = CatBoostRegressor()
model.load_model('model')

# Initialize geocoder
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

        # Calculate distance
        distance = geodesic(
            (pickup_location.latitude, pickup_location.longitude),
            (delivery_location.latitude, delivery_location.longitude)
        ).kilometers

        # Current date and time
        now = datetime.now()
        
        # Prepare prediction data
        prediction_data = {
            'Delivery_person_Age': 30,  # Default value
            'Delivery_person_Ratings': 4.5,  # Default value
            'Delivery_location_latitude': delivery_location.latitude,
            'Delivery_location_longitude': delivery_location.longitude,
            'translogi_latitude': pickup_location.latitude,
            'translogi_longitude': pickup_location.longitude,
            'Weatherconditions': 'Sunny',  # You might want to get this from a weather API
            'Road_traffic_density': 'Medium',  # You might want to get this from a traffic API
            'Vehicle_condition': 1,
            'Type_of_vehicle': 'motorcycle',
            'multiple_deliveries': 0,  # Removed from form, defaulting to 0
            'City': data['city'],
            'Order_day': now.day,
            'Order_month': now.month,
            'Order_year': now.year,
            'Hour_order': now.hour,
            'Min_order': now.minute,
            'distance': distance
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([prediction_data])
        
        # Make prediction
        predicted_time = model.predict(df)[0]
        
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