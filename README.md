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

Paso 1: Registro en la API de OpenWeatherMap

1. Ve al sitio web de [OpenWeatherMap](https://openweathermap.org/api) y
regístrate para obtener una clave de API (API key).
2. Guarda la clave de API, ya que la utilizaremos para hacer consultas a la API.


Paso 2: Instala SQLServer Microsoft:
(si ya esta instalado)
1. Crea una base de datos que llamaremos `weather_db` para almacenar la
información extraída.


PASO 3: PYTHON
1. Clone este repositorio:

   ```bash
   git clone git@github.com:franncardenas/weather_project.git
   ```

2. Instala los paquetes de Python requeridos:

   ```bash
   pip install -r requirements.txt
   ```

Paso 4: Escribir el script de extracción y carga en la
base de datos:
1. Edite el Scrip llamado `extract_transform_load.py` que hará
la extracción de datos desde la API de OpenWeatherMap y los almacenará
en la base de datos SQL Server.
2. Función para extraer datos de la API.
3. Función para transformar los datos.
4. Función para cargar los datos a SQLServer.
5. Proceso ETL.


Paso 5: Verificar los datos en SQLServer:
a. Después de correr el script de Python, puedes verificar que los datos se
hayan cargado correctamente en tu base de datos SQL Server ejecutando
una consulta en SQLServer.
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
