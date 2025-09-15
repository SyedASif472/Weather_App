from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "3dc2de0e2ff336d03023d024e8f3495f"  

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            weather_params = {"q": f"{city},IN","appid": API_KEY,"units": "metric"}
            weather_response = requests.get(weather_url, params=weather_params)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            else:
                weather_data = {"error": "City not found in India!"}

            forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
            forecast_params = {"q": f"{city},IN","appid": API_KEY,"units": "metric"}
            forecast_response = requests.get(forecast_url, params=forecast_params)
            if forecast_response.status_code == 200:
                data = forecast_response.json()
                forecast_data = [item for item in data["list"] if "12:00:00" in item["dt_txt"]]
            else:
                forecast_data = None

    return render_template("index.html", weather=weather_data, forecast=forecast_data, default_city="Bengaluru")

if __name__ == "__main__":
    app.run(debug=True)
