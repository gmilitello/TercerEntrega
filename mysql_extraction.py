import pandas as pd
from dotenv import load_dotenv
import os
import mysql.connector

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def get_city_data_from_mysql(city_name):
    try:
        # Conexión a MySQL
        conn = mysql.connector.connect(
            database=os.getenv("DB_NAME_LOCAL"),
            user=os.getenv("DB_USER_LOCAL"),
            password=os.getenv("DB_PASSWORD_LOCAL"),
            host=os.getenv("DB_HOST_LOCAL"),
            port=os.getenv("DB_PORT_LOCAL")
        )

        # Consulta SQL para obtener datos de la tabla city_data
        query = f"SELECT city, country FROM city_data WHERE city = '{city_name}'"
        
        # Leer datos de la tabla city_data en un DataFrame
        city_data = pd.read_sql(query, conn)

        return city_data
    except Exception as e:
        print("Error al obtener datos de la base de datos MySQL:", e)
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error
    finally:
        # Cerrar la conexión si está abierta
        if 'conn' in locals() and conn.is_connected():
            conn.close()
