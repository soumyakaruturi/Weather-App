from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

load_dotenv()  # load API key

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        units = request.form["units"]

        # Convert units to symbols for UI
        if units == "metric":
            unit_symbol = "C"
        elif units == "imperial":
            unit_symbol = "F"
        else:
            unit_symbol = "K"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            error = data.get("message", "City not found")
        else:
            weather = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": round(data["main"]["temp"], 1),  # Rounded to 1 decimal
                "description": data["weather"][0]["description"].title(),
                "wind": data["wind"]["speed"],
                "humidity": data["main"]["humidity"],
                "unit": unit_symbol
            }

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
