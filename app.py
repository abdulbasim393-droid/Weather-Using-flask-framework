from flask import Flask, render_template, request, session
from utils.weather_services import get_weather, get_forecast
import requests
from config import API_KEY, SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


def choose_theme(weather):
    if not weather:
        return "default"

    condition = weather["weather"][0]["main"].lower()
    temp = weather["main"].get("temp", 0)

    if "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
        return "rainy"
    if "snow" in condition:
        return "snowy"
    if temp >= 30 or "clear" in condition:
        return "warm"
    if "cloud" in condition or "mist" in condition or "fog" in condition:
        return "cloudy"
    return "default"


def update_recent_cities(city):
    if not city:
        return

    city = city.strip()
    if not city:
        return

    cities = session.get("recent_cities", [])
    cities = [existing for existing in cities if existing.lower() != city.lower()]
    cities.insert(0, city)
    session["recent_cities"] = cities[:5]


@app.route("/", methods=["GET", "POST"])
def index():
    city = None
    weather = None
    forecast_24h = []
    error = None
    theme_class = "default"

    recent_cities = session.get("recent_cities", [])

    if request.method == "POST":
        city_input = request.form.get("city")
        if city_input:
            city = city_input.strip()
    elif request.args.get("city"):
        city = request.args.get("city").strip()

    if not city:
        return render_template(
            "index.html",
            city="",
            weather=None,
            forecast=[],
            error=None,
            theme_class="default",
            recent_cities=recent_cities,
        )

    weather = get_weather(city)
    forecast = get_forecast(city)

    if not weather or not forecast:
        error = "Unable to fetch weather data"
        return render_template(
            "index.html",
            error=error,
            city=city,
            weather=None,
            forecast=[],
            theme_class="default",
            recent_cities=recent_cities,
        )

    forecast_24h = forecast["list"][:8]
    theme_class = choose_theme(weather)
    update_recent_cities(city)

    return render_template(
        "index.html",
        city=city,
        weather=weather,
        forecast=forecast_24h,
        error=None,
        theme_class=theme_class,
        recent_cities=session.get("recent_cities", []),
    )

def get_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None


def get_forecast_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    return res.json()



@app.route("/location")
def location_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    recent_cities = session.get("recent_cities", [])

    if not lat or not lon:
        return render_template(
            "index.html",
            error="Location not found",
            city="",
            weather=None,
            forecast=[],
            theme_class="default",
            recent_cities=recent_cities,
        )

    weather = get_weather_by_coords(lat, lon)
    forecast = get_forecast_by_coords(lat, lon)

    if not weather or not forecast:
        return render_template(
            "index.html",
            error="Unable to fetch location weather",
            city="",
            weather=None,
            forecast=[],
            theme_class="default",
            recent_cities=recent_cities,
        )

    city = weather.get("name", "Your Location")
    theme_class = choose_theme(weather)
    update_recent_cities(city)
    forecast_24h = forecast["list"][:8]

    return render_template(
        "index.html",
        city=city,
        weather=weather,
        forecast=forecast_24h,
        error=None,
        theme_class=theme_class,
        recent_cities=session.get("recent_cities", []),
    )


if __name__ == "__main__":
    app.run(debug=True)