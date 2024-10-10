import aiohttp
from database import save_weather_data, session


def parse_weather_data(weather_dict):
    """
    Преобразует словарь с данными о погоде в формат, который может быть сохранен в базе данных.
    """
    # Извлекаем числовое значение температуры
    temperature = float(weather_dict['temperature'].replace(' °C', ''))

    # Разделяем строку "ветер" на скорость и направление
    wind_data = weather_dict['wind'].split(' ')
    wind_speed = float(wind_data[0])
    wind_direction = wind_data[2]

    # Извлекаем давление, удаляя строковые символы
    pressure = float(weather_dict['pressure'].replace(' мм рт. ст.', ''))

    # Осадки: разбиваем на тип и количество
    precipitation_info = weather_dict['precipitation'].split(': ')
    precipitation_type = precipitation_info[0]
    precipitation = float(precipitation_info[1].replace(' мм', ''))

    return {
        'temperature': temperature,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'pressure': pressure,
        'precipitation': precipitation,
        'precipitation_type': precipitation_type
    }


async def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=55.7549&longitude=37.6216"
        "&current=temperature_2m,precipitation,rain,showers,snowfall,surface_pressure,"
        "wind_speed_10m,wind_direction_10m"
        "&wind_speed_unit=ms&timezone=Europe/Moscow&forecast_days=1"
    )

    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            data = await response.json()
            # для отладки print("Fetched weather data:", data)
            # для отладки print("Response details:", response)
            weather_info = extract_weather_info(data)
            # для отладки print(weather_info)
            weather_data = parse_weather_data(weather_info)
            # Пример обработки данных, можно заменить 'session' и 'data['current_weather']' на нужные
            save_weather_data(session, weather_data)


def convert_wind_direction(degree):
    """Функция для преобразования градуса ветра в направление"""
    directions = [
        'С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ'
    ]
    index = round(degree / 45) % 8
    return directions[index]


def convert_pressure(hpa):
    """Функция для преобразования давления из гПа в мм рт. ст."""
    return hpa * 0.75006


def extract_weather_info(data):
    """Функция для извлечения и преобразования нужных данных"""
    current_weather = data['current']

    # Температура в градусах Цельсия
    temperature = current_weather['temperature_2m']

    # Скорость ветра в м/с и его направление
    wind_speed = current_weather['wind_speed_10m']
    wind_direction = convert_wind_direction(current_weather['wind_direction_10m'])

    # Давление в мм ртутного столба
    pressure_hpa = current_weather['surface_pressure']
    pressure_mm = convert_pressure(pressure_hpa)

    # Осадки
    precipitation_type = 'Дождь' if current_weather['rain'] > 0 else 'Без осадков'
    precipitation_amount = current_weather['precipitation']

    return {
        'temperature': f'{temperature} °C',
        'wind': f'{wind_speed} м/с, {wind_direction}',
        'pressure': f'{pressure_mm:.2f} мм рт. ст.',
        'precipitation': f'{precipitation_type}: {precipitation_amount} мм'
    }
