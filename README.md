# weather_project
En este proyecto de ETL (Extracción, Transformación y Carga) de datos meteorológicos, utilizaremos una arquitectura moderna y gratuita con herramientas de alta productividad.


La API pública de
OpenWeatherMap para obtener datos climáticos, Microsoft SQL
Server como base de datos relacional, y Python con sus potentes
bibliotecas para procesar y transformar información. El objetivo
principal es crear un flujo de trabajo eficiente que nos permita
extraer datos meteorológicos en tiempo real, almacenarlos de
manera estructurada y prepararnos para análisis posteriores, todo
utilizando únicamente recursos accesibles y sin costo adicional.
Paso a paso para desarrollar el proyecto:

#Paso 1: Registro en la API de OpenWeatherMap

1. Ve al sitio web de [OpenWeatherMap](https://openweathermap.org/api) y
regístrate para obtener una clave de API (API key).
2. Guarda la clave de API, ya que la utilizaremos para hacer consultas a la API.


#Paso 2: Instala SQLServer Microsoft:
(si ya esta instalado)
1. Crea una base de datos que llamaremos `weather_db` para almacenar la
información extraída.


#PASO 3: PYTHON
1. Clone este repositorio:

   ```bash
   git clone git@github.com:franncardenas/weather_project.git
   ```

2. Instala los paquetes de Python requeridos:

   ```bash
   pip install -r requirements.txt
   ```

# Paso 4: Escribir el Script de Extraccion, Transformacion y Carga (extract_transform_load.py)

a continuacion dejo una breve explicacion del script `extract_transform_load.py`, que se encargara de realizar la **extraccion**, **transformacion** y **carga** de los datos meteorologicos a la base de datos SQL Server.

- 1. Importar las librerias neceesarias

Primero, se necesita importar las librerias que vamos a utilizar en el proyecto:

```python
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
```
- 2. Cargar las variables de entorno
Es importante almacenar las credenciales, como la API Key y la URL de la base de datos, en un archivo .env para mantenerlas seguras. El archivo .env debe contener las siguientes líneas:

```makefile
API_KEY=********
DB_URL=***********
```
Ya en el script, hay que cargar las variables de entorno con la libreria dotenv:

```python
load_dotenv()
api_key = os.getenv("API_KEY")
db_url = os.getenv("DB_URL")
```
- 3. Funcion para extraer los datos de la API
Esta funcion realiza una solicitud GET a la API de OpenWeatherMap para obtener datos meteorologicos en tiempo real. Si la solicitud es exitosa, devuelve los datos en formato JSON.

```python
def extract_weather_data(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error al obtener datos de la API: {response.status_code}')
        return None
```

- 4. Funcion para transformar los datos
Esta funcion toma los datos crudos obtenidos de la API y los convierte en un formato adecuado para ser cargado a la base de datos SQL Server. La transformacion incluye filtrar y dar el formato a los datos que vamos a almacenar.
En mi caso decidi luego de filtrar la ciudad, pais y temperatura actual. Agregar la mnima y maxima de esta ultima, ademas de la humedad, descripcion del tiempo atmosferico y la fecha-hora actual

```python
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
```
- 5. Funcion para cargar los datos a SQL Server
La siguiente funcion carga los datos transformados a la base de datos weather_db en SQL Server. Utilice SQLAlchemy para crear un motor que conecte con la base de datos y la función to_sql() de pandas para insertar los datos.
Ademas de verificar si los datos a insertar ya existen en la base de datos

```python
def load_transformed_data(df):
    if df is not None:
        try:
            df.rename(columns={  ##renombro las columnas del dataframe para que sean iguales a la tabla
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
```
- 6. Función ETL
La función etl encapsula el proceso completo de extracción, transformacion y carga. Esta funcion es la que se ejecutara cuando corramos el script.

```python
def etl(city):
    print(f"** Extrayendo datos del clima de: {city} **")
    raw_data = extract_weather_data(city)
    transformed_data = transform_weather_data(raw_data)
    if transformed_data is not None:
        load_transformed_data(transformed_data)
    else:
        print("No se pudieron cargar los datos")
```
- 7.Ejecutar el script
Por ultimo, agrego la siguiente linea de codigo al final del archivo para ejecutar el script y este reciba el nombre de la ciudad a buscar:

```python
if __name__ == "__main__":
    city = input('Ingrese el nombre de la ciudad que quiere buscar: ')
    etl(city)
```
Esto permite que el script pida al usuario el nombre de la ciudad y ejecute el proceso ETL correspondiente.

# Paso 5: Verificar los datos en SQLServer:
- a. Después de correr el script de Python, puedes verificar que los datos se
hayan cargado correctamente en tu base de datos SQL Server ejecutando
una consulta en SQLServer.
```sql
SELECT * FROM WeatherData;
```
Después de ejecutar el script y hacer la consulta, deberías ver datos similares a los siguientes:
*****

b. Instala la biblioteca de Google BigQuery en tu entorno virtual.
c. Crea un script Python para cargar datos desde SQLserver a BigQuery.
d. Función para extraer los datos de SQL Server.
e. Función para cargar los datos a BigQuery.
f. Proceso ETL a BigQuery.
g. Configura las credenciales para acceder a Google Cloud siguiendo [esta
guía](https://cloud.google.com/docs/authentication/getting-started).

Paso a paso para desarrollar el proyecto:
Opcional: Automatización y Monitoreo
Si deseas automatizar este proceso, podrías usar un cron job en Linux
o el Programador de Tareas en Windows para ejecutar el script en
intervalos regulares.
