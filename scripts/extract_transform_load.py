import os
import pandas as pd
import requests
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv ##CARGO LAS VARIABLES DE ENTORNO


load_dotenv() ##CARGO LAS CREDENCIALES.ENV PARA RECIBIR LA KEY Y LA URL
api_key = os.getenv("API_KEY")
db_url = os.getenv("DB_URL")
engine = create_engine(db_url) ##DECLARO EL MOTOR CON LA CONEXION CON SQLALCHEMY
 

#EXTRIGO LA INFORMACION
def extract_weather_data (city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&&lang=es&appid={api_key}&units=metric'
    response = requests.get(url)
    if (response.status_code == 200):  ##SI ES OK
        data = response.json() ## CONVIERTO EL JSON A UN DICCIONARIO
        return data 
    else:
        print(f'error al obtener respuesta de la API, statuscode:{response.statuscode()} ')
        return None

## PROCESO PARA TRANSFORMAR Y FILTRAR LOS DATOS
def transform_weather_data(data):
    if data is not None:
        ## ARMO EL DATAFRAME FILTRANDO LOS DATOS DE LA API
        weather_data = {
            "city": data['name'],
            "country": data['sys']['country'],
            "current temperature": data['main']['temp'],
            "minimum temperature": data['main']['temp_min'],
            "maximum temperature": data['main']['temp_max'],
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description'],
            "last_update": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') ##GUARDO LA HORA ACTUAL
        }
        return pd.DataFrame([weather_data])
    return None



## PROCESO PARA CARGAR LOS DATOS

def load_transformed_data(df):
    if df is not None:
        try:
            df.rename(columns={  ##renombra las columnas del dataframe
               "city":"city_name",
               "current temperature": "temperature",
               "description": "weather_description",
               "last_update": "date_time"
            }, inplace=True)
         
            df.to_sql('WeatherData', engine, if_exists= 'append', index = False )
         
            print(f'datos cargados en la tabla WeatherData')
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                print(f"Los datos para '{df.iloc[0]['city_name']}' ya existen en la base de datos para la fecha y hora dada.")
            else:
                print(f"Error al cargar los datos a SQL: {str(e)}")
##PROCESO PRINCIPAL
def etl(city):

    print(f"** Extrayendo datos del clima de: {city} **")

    raw_data = extract_weather_data(city) ##GUARDO LOS DATOS EN CRUDO

    transformed_data = transform_weather_data(raw_data) ##GUARDO LOS DATOS TRANSFORMADS

    if transformed_data is not None : ##SI NO ESTA VACIO LO CARGA
        load_transformed_data(transformed_data)
        print("datos cargados correctamente en la base de datos")
    else:
        print("no se pudieron cargar los datos")


city = input('Ingrese el nombre de la ciudad: ')
etl(city)


