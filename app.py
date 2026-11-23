
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_weather():

    api_key = os.environ.get("OPENWEATHER_API_KEY")

    if not api_key:
        return jsonify({"error": "API key not configured"}), 500

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": "Lagos",
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        weather_record = {
            "Location (State)": "Lagos State",
            "Latitude": data["coord"]["lat"],
            "Longitude": data["coord"]["lon"],
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Feels Like": data["main"]["feels_like"],
            "Weather Condition": data["weather"][0]["main"],
            "Wind Speed": data["wind"].get("speed", 0),
            "Wind Direction": data["wind"].get("deg", 0),
            "Wind Gust": data["wind"].get("gust", "")
        }

        return jsonify(weather_record)

    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502
      
