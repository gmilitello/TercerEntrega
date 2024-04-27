import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def get_weather(city):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar errores HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
