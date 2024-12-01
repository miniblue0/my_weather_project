USE [weather_db]
GO

CREATE TABLE WeatherData (
    id INT IDENTITY(1,1) NOT NULL,
    city_name NVARCHAR(100)NOT NULL,
    country NVARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    weather_description NVARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL,
     CONSTRAINT [UC_CityDate] UNIQUE NONCLUSTERED
)
