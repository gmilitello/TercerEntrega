import psycopg2
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def insert_data_into_redshift(city, temperature, humidity, country):
    conn = None  # Definir conn antes del bloque try
    cur = None  # Definir cur antes del bloque try
    try:
        # Conexión a Redshift
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME_REDSHIFT"),
            user=os.getenv("DB_USER_REDSHIFT"),
            password=os.getenv("DB_PASSWORD_REDSHIFT"),
            host=os.getenv("DB_HOST_REDSHIFT"),
            port=os.getenv("DB_PORT_REDSHIFT")
        )

        # Cursor para ejecutar comandos SQL
        cur = conn.cursor()

        # Insertar los datos en la tabla de Redshift
        query = """
            INSERT INTO combined_data (city, temperature, humidity, country, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        timestamp = datetime.now()
        cur.execute(query, (city, temperature, humidity, country, timestamp))

        # Guardar los cambios en la base de datos
        conn.commit()

        print("Datos insertados en Redshift correctamente.")
    except Exception as e:
        print("Error al insertar datos en Redshift:", e)
    finally:
        # Cerrar el cursor y la conexión
        if cur:
            cur.close()
        if conn:
            conn.close()
