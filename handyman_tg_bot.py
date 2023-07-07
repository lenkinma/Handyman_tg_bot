import telebot
import time
from telebot import types

BOT_TOKEN = '6146451826:AAErL9lZgotF3XcC69rl2QXA7ksSUKI-oUs'  # Токен Телеграм-бота
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5  # Таймаут переподключения

# Сообщение при старте
START_MESSAGE = """Привет, я бот на все руки!"""

bd = [{'user_id': '0', 'state': 'default'}]


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

    already_have = False
    for user in bd:
        if user['user_id'] == message.chat.id:
            already_have = True
            user['state'] = 'default'

    if not already_have:
        bd.append({'user_id': message.chat.id, 'state': 'default'})
    print(bd)


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def bot_message(message):
    item_back = types.KeyboardButton('🔙 Назад')
    item1 = types.KeyboardButton('💬 Переводчик')
    item2 = types.KeyboardButton('🔢 Калькулятор')
    item3 = types.KeyboardButton('☁ Погода')
    item4 = types.KeyboardButton('🐸 Мемы')
    item5 = types.KeyboardButton('ℹ Инфо')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in bd:
        if i['user_id'] == message.chat.id:
            user = i

    if message.chat.type == 'private':
        if message.text == '💬 Переводчик':
            markup.add(item_back)
            bot.send_message(message.chat.id, '💬 Переводчик', reply_markup=markup)
            user['state'] = 'translate'

        elif message.text == '🔢 Калькулятор':
            markup.add(item_back)
            bot.send_message(message.chat.id, 'Введите выражение, которое хотите посчитать', reply_markup=markup)
            user['state'] = 'calculate'

        elif message.text == '☁ Погода':
            markup.add(item_back)
            bot.send_message(message.chat.id, '☁ Погода', reply_markup=markup)
            user['state'] = 'weather'

        elif message.text == '🐸 Мемы':
            markup.add(item_back)
            bot.send_message(message.chat.id, '🐸 Мемы', reply_markup=markup)
            user['state'] = 'memes'

        elif message.text == 'ℹ Инфо':
            markup.add(item_back)
            bot.send_message(message.chat.id, 'ℹ Инфо', reply_markup=markup)
            user['state'] = 'info'

        elif message.text == '🔙 Назад':
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, '🔙 Назад', reply_markup=markup)
            user['state'] = 'default'

        else:
            if user['state'] == 'calculate':
                calculator(message)


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
