# ETL de Datos Meteorológicos

Este proyecto es un proceso **ETL (Extract, Transform, Load)** que utiliza la API de OpenWeatherMap para obtener datos meteorológicos en tiempo real de diversas ciudades de Argentina, los transforma en un formato estructurado y los carga en una base de datos SQL. Además, el proceso está automatizado mediante una tarea programada en Windows para ejecutarse diariamente.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Configuración Inicial](#configuración-inicial)
- [Automatización del Proceso](#automatización-del-proceso)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Detalles Técnicos](#detalles-técnicos)
- [Mejoras Futuras](#mejoras-futuras)

---

## Descripción

El script realiza las siguientes etapas:

1. **Extracción**: Obtiene datos en formato JSON desde la API de OpenWeatherMap para un conjunto de ciudades.
2. **Transformación**: Filtra y organiza los datos relevantes (temperatura, descripción del clima, ubicación y hora).
3. **Carga**: Inserta o actualiza los datos en una base de datos SQL, evitando duplicados mediante una consulta `MERGE`.
4. **Automatización**: Se configura una tarea programada en Windows para ejecutar este proceso diariamente.

---

## Tecnologías Utilizadas

- **Python**:
  - `requests` para consumir la API.
  - `pandas` para transformar datos.
  - `sqlalchemy` para interactuar con la base de datos.
  - `dotenv` para la gestion de variables de entorno.
- **Base de Datos**: Microsoft SQL Server.
- **API**: OpenWeatherMap para obtener datos meteorologicos.
- **Sistema Operativo**: Windows (para la tarea programada).

---

## Configuración Inicial

### 1. Clonar el Repositorio
Clona este proyecto desde GitHub:
```bash
git clone <https://github.com/miniblue0/my_weather_project.git>
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar las credenciales en variables de entorno
- Cree un archivo .env en el directorio raiz con las siguientes variables:
- API_KEY: clave de acceso a la API
- DB_URL: url de conexion a la base de datos 'weather_db', deberia quedar algo asi: mssql+pyodbc://<usr>:<pwd>@localhost/weather_db?driver=ODBC+Driver+17+for+SQL+Server
```bash
API_KEY= clave_de_la_api
DB_URL= conexion_a_la_BD 
```
### 4. Automatizacion del proceso:
- 1. Creando un archivo '.bat' con el siguiente contenido para ejecutar el script con una tarea programada:
 ``` bat
 @echo off
cd /d "C:\ruta\alProyecto"
python main.py
```
- 2. Configurar la tarea:
    * Desde el Programador de Tareas en Windows:
        Hay que ir a Crear Tarea>General y ahi se le asigna un nombre, luego en 'Desencadenadores' hay que crear uno nuevo para que la tarea se ejecute diariamente a X hora. En 'Acciones' seleccionamos "Iniciar un programa" y desde ahi buscamos el archivo .bat creado anteriormente. Para finalizar guardamos la tarea.

### 5. Ejecucion del proyecto
- Primero debemos asegurarnos de haber creado la tabla donde se almacenaran los datos ejecutando el sig. script en sql:
``` sql
CREATE TABLE WeatherData (
    city_name NVARCHAR(100),
    country NVARCHAR(50),
    temperature FLOAT,
    weather_description NVARCHAR(255),
    date_time DATETIME,
    PRIMARY KEY (city_name)
)
```

- ***Detalles del proceso ETL**:
    - 1. Extraccion:
            La funcion 'extract_weather_data' realiza la consulta a la API para recibir los datos y retornarlos en formato JSON.
    - 2. Transformacion:
            La funcion 'transform_weather_data' organiza los datos en un DataFrame de Pandas filtrando por datos en concreto.
    - 3. Carga:
            La funcion 'load_transformed_data' ejecuta una query MERGE para insertar o actualizar datos en la tabla WeatherData, asegurando la integridad de los datos y evitando registros duplicados.
    - 4. Automatizacion:
            Logre automatizar el proceso creando un archivo '.bat' y ejecutandolo diariamente con una tarea programada en Windows.