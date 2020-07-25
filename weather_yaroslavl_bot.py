import telebot
import json
import requests
import telebot_calendar
from lxml import etree
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime
from telebot.types import CallbackQuery, ReplyKeyboardRemove

# перед запуском программы создайте telegram-бота
# раскомментируйте следующую строку и внестите в значение TOKEN токен для доступа к HTTP API
# TOKEN = ''

bot = telebot.TeleBot(TOKEN)


# создание календаря с помощью библиотеки telebot_calendar
calendar_1 = telebot_calendar.CallbackData("calendar_1", "action", "year", "month", "day")


# отправка клавиатуры с кнопкой ПОГОДА
@bot.message_handler(commands=['start'])
def sendMessage(message):
    bot.send_message(
        message.chat.id,
        text='Вы можете узнать погоду на любой из ближайших 30-ти дней, нажав на кнопку ПОГОДА',
        reply_markup=keyboard(),
    )


# обработка входящих сообщений, предоставление возможности выбора даты
@bot.message_handler(content_types=['text'])
def weather(message):
    # обработка кнопки ПОГОДА
    if message.text == "ПОГОДА":
        # получение текущей даты для формирования календаря
        now = datetime.now()
        # отправка сообщения с inline-каледарем
        bot.send_message(
            message.chat.id,
            'Вы можете узнать погоду на любой из ближайших 30-ти дней. Пожалуйста, выберите дату.',
            reply_markup=telebot_calendar.create_calendar(
                name=calendar_1.prefix,
                year=now.year,
                month=now.month,
            ),
        )


# обраотка выбора даты пользователем с помощью библиотеки telebot_calendar
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = telebot_calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        # вероятно этот фрагмент обработки допустимых дат можно сделать короче, но я займусь этим потом
        d1 = date.today().strftime('%d.%m.%Y')
        d2 = date.strftime('%d.%m.%Y')
        d1 = datetime.strptime(d1, "%d.%m.%Y")
        d2 = datetime.strptime(d2, "%d.%m.%Y")

        # обработка допустимых дат: сообщение будет отправлено в случае, если выбранная дата из следуюих 30-ти дней
        if d2 > d1 and int((d2 - d1).days) <= 30:
            # отправка сообщения с погодой на выбранный день
            bot.send_message(
                chat_id=call.from_user.id,
                # вызов функции, возвращающей погоду на выбранный день
                text=get_weather(int(f"{date.strftime('%d')}")),
            )

        # в случае, если дата не в области допустимых, производится отправка сообщения по-умолчанию
        else:
            bot.send_message(
                chat_id=call.from_user.id,
                text="На выбранную дату прогноз недоступен",
            )

    # в случае, если пользователь отменил выбор даты
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Отмена",
        )



# получение погоды с сайта yandex.ru и возврат сформированного текста с прогнозом на выбранный день
def get_weather(day):
    # запрос к сайту yandex.ru
    response = requests.get(
        'https://yandex.ru/pogoda/16/month',
    )
    # получение текста ответа
    html = response.text

    # фрагмент парсинга html-кода web-страницы
    soup = BeautifulSoup(html, 'html.parser')
    # получение тега div, содержащего необходимые параметры погоды на месяц
    find_text = soup.find_all('div', {'class': 'climate-graph'})
    # получение параметра data-bem, содержащего параметры погоды на месяц
    elem = etree.fromstring(str(find_text[0]))
    weather_dict = elem.get('data-bem')
    weather_dict = dict(json.loads(weather_dict))
    # получение списка словарей с необходимыми параметрами погоды на месяц
    weather_list = weather_dict['climate-graph']['graphData']

    # перебор списка словерей
    for daily in weather_list:
        # поиск словаря с заданным днем в списке; формирование ответа на основе словаря с параметрами погоды на день
        if daily['day'] == day:
            message = f"ПРОГНОЗ ПОГОДЫ НА {daily['day']} {daily['monthName'].upper()} \n"
            message += f"Днем: {daily['max_day_t']} \n"
            message += f"Ночью: {daily['min_night_t']} \n"
            message += f"Вероятность осадков: {daily['prec_prob']}% \n"
            message += f"Атмосферное давление: {daily['pressure']} мм. рт. ст. \n"
            message += f"Влажность: {daily['humidity']}% \n"
            return message


# формирование клавиатуры с кнопкой ПОГОДА
def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('ПОГОДА')
    markup.add(btn1)
    return markup



# запуск бота
bot.polling(none_stop=True)