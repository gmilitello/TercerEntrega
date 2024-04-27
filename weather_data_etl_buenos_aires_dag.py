from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from api_extraction import get_weather
from mysql_extraction import get_city_data_from_mysql
from redshift_transform_load import insert_data_into_redshift
from send_email import send_email

# Define los argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define la conexión del DAG
with DAG(
    'tp_final_ing_datos',
    default_args=default_args,
    description='TP Final Ingestion de Datos',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    # Extraer datos del clima
    extract_weather_task = PythonOperator(
        task_id='extract_weather',
        python_callable=get_weather,
        op_kwargs={'city': 'Buenos Aires'},
    )

    # Extraer datos de MySQL
    extract_mysql_task = PythonOperator(
        task_id='extract_mysql',
        python_callable=get_city_data_from_mysql,
        op_kwargs={'city_name': 'Buenos Aires'},
    )

    # Transformar y cargar datos en Redshift
    transform_load_redshift_task = PythonOperator(
        task_id='transform_load_redshift',
        python_callable=insert_data_into_redshift,
        op_kwargs={'city': 'Buenos Aires'},
    )

    # Enviar email de confirmación
    send_email_task = PythonOperator(
        task_id='send_email',
        python_callable=send_email,
    )

    # Define la secuencia de tareas
    extract_weather_task >> extract_mysql_task >> transform_load_redshift_task >> send_email_task