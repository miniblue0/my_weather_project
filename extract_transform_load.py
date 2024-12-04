import os
import pandas as pd
import requests
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime


load_dotenv() #cargo las variables de entorno
api_key = os.getenv("API_KEY") #llave de la api
db_url = os.getenv("DB_URL") #url de la base de datos
engine = create_engine(db_url) #motor de la conexion a sql


#extraigo los datos de la api y retorno un diccionario
def extract_data(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error al obtener respuesta de la API, status code: {response.status_code}")
        return None


#filtro y transformo los datos
def transform_data(data):
    if data is not None:
       
        data = {
            "city_name": data['name'],
            "country": data['sys']['country'],
            "temperature": data['main']['temp'],
            "weather_description": data['weather'][0]['description'],
            "date_time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')  #fecha y hora actual
        }
        return pd.DataFrame([data])
    return None


#cargo los datos transformados y con una query comparo las filas

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
                    """) #use un MERGE para comparar en ambos casos y actualizar o insertar segun corresponda

                        #hago la verificacion del dataframe y la tabla. luego inserta/actualiza
                    connection.execute(UPSERT, {
                        "city_name": row['city_name'],
                        "country": row['country'],
                        "temperature": row['temperature'],
                        "weather_description": row['weather_description'],
                        "date_time": row['date_time']
                    })

                    #commit para guardar los cambios
                    connection.commit()

            print(f"Datos cargados/actualizados en la tabla WeatherData")
        except Exception as e:
            print(f"Error al cargar los datos a SQL: {str(e)}")

#funcion principal
def etl(city):
    print(f"** Extrayendo datos del clima de: {city} **")
    raw_data = extract_data(city)
    if raw_data is not None:
        print("** Datos extraidos correctamente")
    transformed_data = transform_data(raw_data)
    if transformed_data is not None:
        load_transformed_data(transformed_data)
    else:
        print("No se pudieron cargar los datos")

#ejecuto el script y cargo/actualizo una lista de ciudades
if __name__ == "__main__":
    ciudades = ['Buenos Aires','Corrientes', 'Rosario','Cordoba','Mendoza','San Juan','La Plata', 'El Bolson', 'Bariloche', 'Mar del Plata']
    for ciudad in ciudades:
        etl(ciudad)