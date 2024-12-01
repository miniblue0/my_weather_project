# ETL de Datos Meteorológicos

Este proyecto es un proceso **ETL (Extract, Transform, Load)** que utiliza la API de OpenWeatherMap para obtener datos meteorologicos en tiempo real de diversas ciudades del mundo (en mi caso utilice solo ciudades de Argentina), los filtra y transforma en un formato estructurado para luego cargarlos en una tabla de SQL. Ademas, me tome el tiempo de automatizar el proceso con una tarea programada en Windows para ejecutarse diariamente.

## Tabla de Contenidos

- [Descripcion](#descripcion)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configuracion Inicial](#configuracion-inicial)
- [Automatizacion del Proceso](#automatizacion-del-proceso)
- [Ejecucion del Proyecto](#ejecucion-del-proyecto)
- [Detalles del proceso ETL](#Detalles-del-proceso-ETL)

---

## Descripcion

El script realiza las siguientes etapas:

1. **Extraccion**: Obtiene datos en formato JSON desde la API de OpenWeatherMap para un conjunto de ciudades.
2. **Transformacion**: Filtra y organiza los datos relevantes (temperatura, descripción del clima, ubicación y hora).
3. **Carga**: Inserta o actualiza los datos en una base de datos SQL, evitando duplicados mediante una consulta `MERGE`.
4. **Automatizacion**: Si bien este paso era opcional me parecio un buen detalle a agregar al proyecto. Utilice un archivo `.bat` y el programador de tareas de windows

---

## Tecnologias Utilizadas

- **Python**:
  - `requests` para consumir la API.
  - `pandas` para transformar datos.
  - `sqlalchemy` para interactuar con la base de datos.
  - `dotenv` para la gestion de variables de entorno.
- **Base de Datos**: Microsoft SQL Server.
- **API**: OpenWeatherMap para obtener datos meteorologicos.
- **Sistema Operativo**: Windows (para la tarea programada).

---

## Configuracion Inicial

### 1. Clonar el Repositorio
Clona este proyecto desde GitHub:
```bash
git clone <https://github.com/miniblue0/my_weather_project.git>
```

---

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```
---

### 3. Configurar las credenciales en variables de entorno
- Cree un archivo `.env` en el directorio raiz con las siguientes variables:
- `API_KEY` : clave de acceso a la API
- `DB_URL` : url de conexion a la base de datos `weather_db`, deberia quedar algo asi: `mssql+pyodbc://<usr>:<pwd>@localhost/weather_db?driver=ODBC+Driver+17+for+SQL+Server`
```bash
API_KEY= clave_de_la_api
DB_URL= conexion_a_la_BD 
```
---

### 4. Automatizacion del proceso:
- 1. Creando un archivo `.bat` con el siguiente contenido para ejecutar el script con una tarea programada:
 ``` bat
 @echo off
cd /d "C:\ruta\al\repositorio"
python extract_transform_load.py
```
- 2. Configurar la tarea:
    * Desde el Programador de Tareas en Windows:
        Hay que ir a Crear Tarea>General y ahi se le asigna un nombre, luego en 'Desencadenadores' hay que crear uno nuevo para que la tarea se ejecute diariamente a X hora. En 'Acciones' seleccionamos "Iniciar un programa" y desde ahi buscamos el archivo .bat creado anteriormente. Para finalizar guardamos la tarea.

---

### 5. Ejecucion del proyecto:
- Primero hay que asegurarse de haber creado la tabla donde se almacenaran los datos ejecutando el sig. script en sql:
``` sql
CREATE TABLE WeatherData (
    id INT IDENTITY(1,1) NOT NULL,
    city_name NVARCHAR(100)NOT NULL,
    country NVARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    weather_description NVARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL,
     CONSTRAINT [UC_CityDate] UNIQUE NONCLUSTERED
)
```
---

### 6. Detalles del proceso ETL:
- 1. Extraccion:
    La funcion `extract_weather_data` realiza la consulta a la API para recibir los datos y retornarlos en formato JSON.
- 2. Transformacion:
    La funcion `transform_weather_data` organiza los datos en un DataFrame de Pandas filtrando por datos en concreto.
- 3. Carga:
    La funcion `load_transformed_data` ejecuta una query `MERGE` para insertar o actualizar datos en la tabla `WeatherData`, asegurando la integridad de los datos y evitando registros duplicados.
- 4. Automatizacion:
    Logre automatizar el proceso creando un archivo `.bat` y ejecutandolo diariamente con una tarea programada en Windows.