#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
from pathlib import Path
import logging
from json import JSONDecodeError

# Настройка логирования
logger = logging.getLogger('FlightLogger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('flights.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

default_data_file = "flights.json"

def input_flights():
    flights = []
    try:
        n = int(input("Введите количество рейсов: "))
        logger.info(f"Пользователь ввел количество рейсов: {n}")
    except ValueError as ve:
        logger.error("Некорректный ввод количества рейсов.", exc_info=True)
        print("Ошибка: количество рейсов должно быть целым числом.")
        return flights

    for i in range(n):
        flight = {}
        try:
            flight["город назначения"] = input("Введите город назначения: ")
            flight["номер рейса"] = input("Введите номер рейса: ")
            flight["тип самолета"] = input("Введите тип самолета: ")
            flights.append(flight)
            logger.info(f"Добавлен рейс: {flight}")
        except Exception as e:
            logger.error(f"Ошибка при вводе данных рейса #{i+1}.", exc_info=True)
            print(f"Ошибка при вводе данных рейса #{i+1}. Попробуйте снова.")
    flights.sort(key=lambda x: x.get("город назначения", ""))
    logger.info("Рейсы отсортированы по городу назначения.")
    return flights

def print_flights_with_plane_type(flights):
    try:
        plane_type = input("Введите тип самолета: ")
        logger.info(f"Пользователь запросил рейсы с типом самолета: {plane_type}")
    except Exception as e:
        logger.error("Ошибка при вводе типа самолета.", exc_info=True)
        print("Ошибка при вводе типа самолета.")
        return

    found = False
    for flight in flights:
        if flight.get("тип самолета") == plane_type:
            print(f"Город назначения: {flight.get('город назначения')}, Номер рейса: {flight.get('номер рейса')}")
            logger.info(f"Найден рейс: {flight}")
            found = True
    if not found:
        print("Рейсы с указанным типом самолета не найдены")
        logger.info(f"Рейсы с типом самолета '{plane_type}' не найдены.")

def save_data_to_json(flights, data_file):
    try:
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump(flights, file, ensure_ascii=False, indent=4)
        logger.info(f"Данные успешно сохранены в {data_file}")
    except IOError as ioe:
        logger.error(f"Ошибка при сохранении данных в файл {data_file}.", exc_info=True)
        print(f"Ошибка при сохранении данных в файл {data_file}.")

def load_data_from_json(data_file):
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Данные успешно загружены из {data_file}")
            return data
        except JSONDecodeError as jde:
            logger.error(f"Ошибка декодирования JSON из файла {data_file}.", exc_info=True)
            print(f"Ошибка: файл {data_file} содержит некорректные данные.")
            return []
        except IOError as ioe:
            logger.error(f"Ошибка при чтении файла {data_file}.", exc_info=True)
            print(f"Ошибка при чтении файла {data_file}.")
            return []
    else:
        logger.warning(f"Файл данных {data_file} не найден. Возвращается пустой список рейсов.")
        return []

def main():
    parser = argparse.ArgumentParser(description='Manage flight data')
    parser.add_argument('--input', action='store_true', help='Input new flight data')
    parser.add_argument('--print_plane_type', action='store_true', help='Print flights with specific plane type')
    args = parser.parse_args()

    # Получаем путь к домашнему каталогу пользователя
    home_dir = Path.home()
    data_file = home_dir / default_data_file
    logger.info(f"Используемый файл данных: {data_file}")

    try:
        if args.input:
            flights = input_flights()
        else:
            flights = load_data_from_json(data_file)

        if args.print_plane_type:
            print_flights_with_plane_type(flights)

        save_data_to_json(flights, data_file)
    except Exception as e:
        logger.critical("Непредвиденная ошибка в основной функции.", exc_info=True)
        print("Произошла непредвиденная ошибка. Пожалуйста, проверьте лог файл для деталей.")

if __name__ == "__main__":
    main()
