
import pandas as pd
from pathlib import Path
from flask_cors import CORS
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
from src.pipeline.prediction import 

app = Flask(__name__)
CORS(app)

model = Path("Artifacts/model/best_model.pkl")

geolocator = Nominatim(user_agent="delivery_app")