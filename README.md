# Погода в Ярославле

![Python Version](https://img.shields.io/badge/Python-3.8-blue)

## Установка
Для работы программы необходим Python версии 3.8. 

Также потребуются библиотеки, указанные в [requirement.txt](https://github.com/BArrZik/yaroslavl_weather_bot/blob/master/requirements.txt).

Библиотеки можно установить с помощью:
```
pip3 install [package-name==version]
```

## Преднастройка и запуск
В файле [weather_yaroslavl_bot.py](https://github.com/BArrZik/yaroslavl_weather_bot/blob/master/weather_yaroslavl_bot.py) подставьте в переменную [TOKEN] токен для доступа к HTTP API


В консоли перейдите в папку, где хранится файл [weather_yaroslavl_bot.py](https://github.com/BArrZik/yaroslavl_weather_bot/blob/master/weather_yaroslavl_bot.py) и запустите программу:
```
python3 weather_yaroslavl_bot.py
```

## Использование
После нажатия конпки [старт]() появляется кнопка [ПОГОДА](). 

При нажатии кнопки [ПОГОДА]() пользователю приходит inline-календарь с возможностью выбора даты. 

После выбора пользователем даты из допустимого диапазона, пользователь получает прогноз на выбранную дату. 
