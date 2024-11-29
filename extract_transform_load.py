import os
import pandas as pd
import requests
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# Cargar las variables de entorno
load_dotenv()
api_key = os.getenv("API_KEY")
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

# Función para extraer los datos de la API
def extract_weather_data(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error al obtener respuesta de la API, status code: {response.status_code}")
        return None

# Función para transformar los datos
def transform_weather_data(data):
    if data is not None:
        # Filtrar y estructurar los datos necesarios
        weather_data = {
            "city_name": data['name'],
            "country": data['sys']['country'],
            "temperature": data['main']['temp'],
            "weather_description": data['weather'][0]['description'],
            "date_time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')  # Hora actual
        }
        return pd.DataFrame([weather_data])
    return None

# Función para cargar los datos en la base de datos
def load_transformed_data(df):
    if df is not None:
        try:
            with engine.connect() as connection:
                for _, row in df.iterrows():
                    # Convertir `date_time` al tipo `datetime`
                    row['date_time'] = datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M:%S')
                                        # Primero eliminar el registro si existe para esa ciudad y fecha
                    delete_query = text("""
                        DELETE FROM WeatherData
                        WHERE city_name = :city_name
                    """)
                    connection.execute(delete_query, {
                        "city_name": row['city_name'],
                    })

                    # Query MERGE para insertar o actualizar los datos
                    UPSERT = text("""
                        MERGE INTO WeatherData AS target
                        USING (SELECT :city_name AS city_name,
                                    :country AS country,
                                    :temperature AS temperature,
                                    :weather_description AS weather_description,
                                    :date_time AS date_time) AS source
                        ON target.city_name = source.city_name  -- Comparar solo por city_name
                        WHEN MATCHED THEN
                            UPDATE SET 
                                country = source.country,
                                temperature = source.temperature,
                                weather_description = source.weather_description,
                                date_time = source.date_time
                        WHEN NOT MATCHED THEN
                            INSERT (city_name, country, temperature, weather_description, date_time)
                            VALUES (source.city_name, source.country, source.temperature, source.weather_description, source.date_time);
                    """)

                    # Ejecutar el query con los parámetros
                    print("Ejecutando el MERGE...")
                    connection.execute(UPSERT, {
                        "city_name": row['city_name'],
                        "country": row['country'],
                        "temperature": row['temperature'],
                        "weather_description": row['weather_description'],
                        "date_time": row['date_time']
                    })
                    connection.commit()

            print(f"Datos cargados/actualizados en la tabla WeatherData")
        except Exception as e:
            print(f"Error al cargar los datos a SQL: {str(e)}")

# Función principal ETL
def etl(city):
    print(f"** Extrayendo datos del clima de: {city} **")
    raw_data = extract_weather_data(city)
    transformed_data = transform_weather_data(raw_data)
    if transformed_data is not None:
        load_transformed_data(transformed_data)
    else:
        print("No se pudieron cargar los datos")

# Iniciar el script
if __name__ == "__main__":
    city = input("Ingrese el nombre de la ciudad que quiere buscar: ")
    etl(city)
