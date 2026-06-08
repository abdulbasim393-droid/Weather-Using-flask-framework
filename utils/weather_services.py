import requests
from config import API_KEY


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return None

        return res.json()

    except:
        return None


def get_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return None

        return res.json()

    except:
        return None