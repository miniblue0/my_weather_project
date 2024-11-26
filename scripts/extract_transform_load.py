import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv() ##CARGO LAS VARIBALES DE ENTORNO 
api_key = os.getenv("API_KEY") #IMPORTO LA API_KEY
db_url = os.getenv("DB_URL")
engine = create_engine(db_url) 

def extract_weather_data(api_key, city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&&lang=es&appid={api_key}&units=metric'
    response = requests.get(url)
    if (response.status_code == 200):
        data = response.json()
        print(data)
        return data
    else:
        print(f'error al obtener respuesta de la API, statuscode: {response.statuscode()}')
        return None

city_name = input('Ingrese el nombre de la ciudad: ')
extract_data(api_key,city_name)
