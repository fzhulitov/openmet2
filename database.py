from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime


Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)  # Температура в градусах Цельсия
    wind_speed = Column(Float)  # Скорость ветра в м/с
    wind_direction = Column(String)  # Направление ветра
    pressure = Column(Float)  # Давление в мм рт. ст.
    precipitation = Column(Float)  # Количество осадков в мм
    precipitation_type = Column(String)  # Тип осадков (дождь/снег/без осадков)


# Настройка базы данных
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def save_weather_data(session, weather_data):
    """
    Сохраняет данные о погоде в базу данных.
    """

    # Создаем экземпляр класса WeatherData
    weather_entry = WeatherData(
        temperature=weather_data['temperature'],
        wind_speed=weather_data['wind_speed'],
        wind_direction=weather_data['wind_direction'],
        pressure=weather_data['pressure'],
        precipitation=weather_data['precipitation'],
        precipitation_type=weather_data['precipitation_type']
    )

    # Добавляем и сохраняем данные в сессии
    session.add(weather_entry)
    session.commit()
