import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey123")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")