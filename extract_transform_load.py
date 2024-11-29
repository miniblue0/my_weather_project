import os
import pandas as pd
import requests
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

#CARGO LAS VARIABLES DE ENTORNO CON LAS CREDENCIALES
load_dotenv()
api_key = os.getenv("API_KEY")
db_url = os.getenv("DB_URL")
engine = create_engine(db_url) #DECLARO EL MOTOR CON LA CONEXION A SQL


#FUNCION PARA EXTRAER LOS DATOS DE LA API EN FORMATO JSON

def extract_weather_data(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error al obtener respuesta de la API, status code: {response.status_code}")
        return None


#FUNCION PARA TRANSFORMAR EL JSON A UN DATAFRAME
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


#CARGO LOS DATOS TRANSFORMADOS Y CON UNA QUERY VERIFICO PARA EVITAR DUPLICADOS

def load_transformed_data(df):
    if df is not None:
        try:
            with engine.connect() as connection:
                for _, row in df.iterrows():

                    row = row.copy() #tuve que hacer una copia de la fila porque tenia este error 'SettingWithCopyWarning '

                    #vuelvo a formatear la fecha y hora
                    row['date_time'] = datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M:%S')
                    
                    
                    print(f"Insertando/actualizando datos: city_name={row['city_name']}, temperature={row['temperature']}, date_time={row['date_time']}")

                    #arme la query upsert para verificar si la ciudad ya existe sea actualizada, y sino sea insertada
                    UPSERT = text("""
                        MERGE INTO WeatherData AS target 
                        USING (SELECT :city_name AS city_name,
                                    :country AS country,
                                    :temperature AS temperature,
                                    :weather_description AS weather_description,
                                    :date_time AS date_time) AS source
                        ON target.city_name = source.city_name
                        WHEN MATCHED THEN
                            UPDATE SET 
                                country = source.country,
                                temperature = source.temperature,
                                weather_description = source.weather_description,
                                date_time = source.date_time
                        WHEN NOT MATCHED THEN
                            INSERT (city_name, country, temperature, weather_description, date_time)
                            VALUES (source.city_name, source.country, source.temperature, source.weather_description, source.date_time);
                    """) #use un MERGE para comparar en ambos casos y ejecutar o insrtar segun corresponda

                        #hago la verificacion del dataframe y la tabla
                    connection.execute(UPSERT, {
                        "city_name": row['city_name'],
                        "country": row['country'],
                        "temperature": row['temperature'],
                        "weather_description": row['weather_description'],
                        "date_time": row['date_time']
                    })

                    #tuve que usar commit porque no se modificaba la tabla 
                    connection.commit()

            print(f"Datos cargados/actualizados en la tabla WeatherData")
        except Exception as e:
            print(f"Error al cargar los datos a SQL: {str(e)}")

#funcion principal 
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
    ciudades = ['Buenos Aires', 'Rosario','Cordoba','Mendoza','San Juan','La Plata' ]
    for ciudad in ciudades:
        etl(ciudad)