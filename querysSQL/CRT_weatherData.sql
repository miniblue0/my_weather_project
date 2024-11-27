--CREATE DATABASE weather_db;

USE [weather_db]
GO

/****** Object:  Table [dbo].[WeatherData]    Script Date: 27/11/2024 19:12:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[WeatherData](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[city_name] [varchar](100) NOT NULL,
	[country] [varchar](100) NOT NULL,
	[temperature] [float] NOT NULL,
	[minimum temperature] [float] NOT NULL,
	[maximum temperature] [float] NOT NULL,
	[humidity] [int] NOT NULL,
	[weather_description] [varchar](255) NOT NULL,
	[date_time] [datetime] NOT NULL,
 CONSTRAINT [unique_city_datetime] UNIQUE NONCLUSTERED 
(
	[city_name] ASC,
	[date_time] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

