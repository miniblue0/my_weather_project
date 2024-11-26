CREATE TABLE WeatherData (
    id INT PRIMARY KEY IDENTITY(1,1),
    city_name NVARCHAR(50),
    temperature FLOAT,
    humidity INT,
    weather_description NVARCHAR(255),
    date_time DATETIME
);
