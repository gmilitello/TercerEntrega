from api_extraction import get_weather
from mysql_extraction import get_city_data_from_mysql
from redshift_transform_load import insert_data_into_redshift
from send_email import send_email
from datetime import datetime
import pandas as pd

def main(city):
    # Extraer datos de la API
    data_from_api = get_weather(city)
    temperature = data_from_api['main']['temp']
    humidity = data_from_api['main']['humidity']
    country = data_from_api['sys']['country']

    # Extraer datos de la base de datos MySQL
    city_data = get_city_data_from_mysql(city)

    if not city_data.empty:
        country = city_data['country'].iloc[0]

    # Transformar y cargar datos en Amazon Redshift
    insert_data_into_redshift(city, temperature, humidity, country)

    # Enviar correo electrónico si la temperatura es menor a 20°C
    if temperature < 20:
        subject = "Alerta de Temperatura"
        body = f"La temperatura en {city} es {temperature}°C, está por debajo de 20°C."
        send_email(subject, body)

if __name__ == "__main__":
    city = "Buenos Aires"  # Puedes cambiar la ciudad aquí
    main(city)
