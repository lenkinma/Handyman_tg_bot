import math
from bs4 import BeautifulSoup
import requests
import telebot
import time
from telebot import types
from googletrans import Translator
import random

BOT_TOKEN = '6146451826:AAErL9lZgotF3XcC69rl2QXA7ksSUKI-oUs'  # Токен Телеграм-бота
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5  # Таймаут переподключения

# Сообщение при старте
START_MESSAGE = """Привет, я бот на все руки!"""

bd = [{'user_id': '0', 'state': 'default'}]


def make_bd(message):
    already_have = False
    for user in bd:
        if user['user_id'] == message.chat.id:
            already_have = True

    if not already_have:
        bd.append({'user_id': message.chat.id, 'state': 'default'})
    print(bd)


# Обработчик сообщений-команд
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('💬 Переводчик')
    item2 = types.KeyboardButton('🔢 Калькулятор')
    item3 = types.KeyboardButton('☁ Погода')
    item4 = types.KeyboardButton('🐸 Мемы')
    item5 = types.KeyboardButton('ℹ Инфо')

    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Привет! Я бот! Чем тебе помочь?', reply_markup=markup)

    make_bd(message)



# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def bot_message(message):
    item_back = types.KeyboardButton('🔙 Назад')
    item1 = types.KeyboardButton('💬 Переводчик')
    item2 = types.KeyboardButton('🔢 Калькулятор')
    item3 = types.KeyboardButton('☁ Погода')
    item4 = types.KeyboardButton('🐸 Мемы')
    item5 = types.KeyboardButton('ℹ Инфо')
    item6 = types.KeyboardButton('⏰ Мем из 2011')
    item7 = types.KeyboardButton('💎 IT мем')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    make_bd(message)

    for i in bd:
        if i['user_id'] == message.chat.id:
            user = i

    if message.chat.type == 'private':
        if message.text == '💬 Переводчик':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите выражение, которое хотите перевести', reply_markup=markup)
            user['state'] = 'translate'

        elif message.text == '🔢 Калькулятор':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите выражение, которое хотите посчитать', reply_markup=markup)
            user['state'] = 'calculate'

        elif message.text == '☁ Погода':
            markup.add(item_back, item5)
            bot.send_message(message.chat.id, 'Введите город, в котором хотите узнать погоду', reply_markup=markup)
            user['state'] = 'weather'

        elif message.text == '🐸 Мемы':
            markup.add(item_back, item6, item7, item5)
            bot.send_message(message.chat.id, 'Бот может прислать рандомный мем из двух пабликов в вк на выбор!', reply_markup=markup)
            user['state'] = 'memes'
        elif message.text == '⏰ Мем из 2011':
            memes(message, 1)
        elif message.text == '💎 IT мем':
            memes(message, 2)

        elif message.text == 'ℹ Инфо':
            if user['state'] == 'default':
                bot.send_message(message.chat.id, 'Авторы бота: \n@kuuorti \n@lenkinmax')
            elif user['state'] == 'calculate':
                bot.send_message(message.chat.id, 'Вам доступны базовые арифметические операци \n\nВы также можете использовать скобки, если они вам понадобятся')
            elif user['state'] == 'translate':
                bot.send_message(message.chat.id, 'В боте доступно два языка: RU, EN \n\nБот автоматически определит язык и отправит перевод')
            elif user['state'] == 'weather':
                bot.send_message(message.chat.id, 'Бот знает погоду во всех городах мира, \n\nНазвания городов можно вводить с использованием кириллицы')
            elif user['state'] == 'memes':
                bot.send_message(message.chat.id, 'Бот умеет скидывать рандомный мем из пабликов ВК \n\n(Если вам выдаст ошибку, то скорее всего это траблы со стороны ВК)')

        elif message.text == '🔙 Назад':
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, '🔙 Назад', reply_markup=markup)
            user['state'] = 'default'

        else:
            if user['state'] == 'calculate':
                calculator(message)
            elif user['state'] == 'translate':
                translator(message)
            elif user['state'] == 'weather':
                weather(message)
            elif user['state'] == 'memes':
                memes(message)


# мемы
def memes(message, public):
    accept = False
    errors = 0
    while not accept:
        random_number = random.randint(0, 2000)
        if public == 1:
            public1 = 457263933 - random_number;
            url = f'https://vk.com/memsfrom2k11?z=photo-132938840_{public1}%2Falbum-132938840_00%2Frev' # для мемов из 2011
        else:
            public1 = 457239992 - random_number;
            url = f'https://vk.com/prog_memes?z=photo-205359325_{public1}' # для IT мемов
        try:
            response = requests.get(url)
            bs = BeautifulSoup(response.text, "lxml")
            img = bs.find('a', 'PhotoviewPage__photo').find('img').attrs['src']
            bot.send_photo(message.chat.id, img)
            accept = True
        except:
            errors += 1
            if errors == 30:
                accept = True
                bot.send_message(message.chat.id, 'Что-то пошло не так!\n\nПопробуйте еще раз')


# погода
def weather(message):
    weather_api_key = '54e6869ab9c8a14b92e5ada3bbd43ee6'
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid={weather_api_key}")
        data = response.json()

        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        bot.send_message(message.chat.id, f"Погода в городе: {city}\nТемпература: {cur_temp}°C\nВлажность: {humidity}%\nДавление: {math.ceil(pressure/1.333)} мм.рт.ст\nВетер: {wind} м/с \nХорошего дня!")
    except:
        bot.send_message(message.chat.id, 'Проверьте название города!')


# переводчик
def translator(message):
    translator = Translator()

    # Определение языка ввода.
    lang = translator.detect(message.text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    if lang == 'ru':
        send = translator.translate(message.text)
        bot.send_message(message.chat.id, send.text)

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(message.text, dest='ru')
        bot.send_message(message.chat.id, send.text)


# калькулятор
def calculator(message):
    msg = None

    user_message = message.text.lower()
    user_message = user_message.lstrip()
    user_message = user_message.rstrip()

    try:
        answer = str(eval(user_message.replace(' ', '')))
        msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)
    except SyntaxError:
        msg = bot.send_message(message.chat.id,
                               'Похоже, что вы написали что-то не так. \nИсравьте ошибку и повторите снова')
    except NameError:
        msg = bot.send_message(message.chat.id,
                               'Переменную которую вы спрашиваете я не знаю. \nИсравьте ошибку и повторите снова')
    except TypeError:
        msg = bot.send_message(message.chat.id,
                               'Мне кажется, что в выражении присутствует ошибка типов. \nИсравьте ошибку и повторите снова')
    except ZeroDivisionError:
        msg = bot.send_message(message.chat.id,
                               'В выражении вы делите на ноль. \nИсравьте ошибку и повторите снова')


# Вход в программу
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('Ошибка подключения. Попытка подключения через %s сек.' % TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)
