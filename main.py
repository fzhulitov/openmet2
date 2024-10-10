import asyncio
import pandas as pd
from weather import fetch_weather
from database import session, WeatherData


async def periodic_weather_request(interval):
    while not stop_event.is_set():
        await fetch_weather()
        await asyncio.sleep(interval)


def export_to_excel():
    # Получаем последние 10 записей из базы данных, отсортированных по времени
    data = session.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(10).all()

    # Преобразуем данные в DataFrame для удобного экспорта
    df = pd.DataFrame([{
        'Timestamp': record.timestamp,
        'Temperature': record.temperature,
        'Wind Speed': record.wind_speed,
        'Wind Direction': record.wind_direction,
        'Pressure': record.pressure,
        'Precipitation': record.precipitation,
        'Precipitation Type': record.precipitation_type
    } for record in data])

    # Экспортируем данные в Excel-файл
    df.to_excel('weather_data.xlsx', index=False)


stop_event = asyncio.Event()


async def command_handler():
    while True:
        command = await asyncio.to_thread(input, "Введите команду: ")  # Ввод в отдельном потоке
        if command == "export":
            print("Выполняется экспорт данных...")
            export_to_excel()  # Экспорт данных в Excel
        elif command == "exit":
            stop_event.set()
            print("Завершение работы.")
            break
        else:
            print("Неизвестная команда")

# Запуск сбора данных и команды экспорта


async def main():
    # Запуск обоих процессов параллельно
    await asyncio.gather(
        periodic_weather_request(180),
        command_handler()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
