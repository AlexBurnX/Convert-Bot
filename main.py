# Телеграм бот: ConvertBot v1.0
# Ссылка: https://t.me/ConvertRusBot

import telebot
from config import *
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'старт', 'помощь', 'хелп'])
def helps(message: telebot.types.Message):
    text = 'ℹ Помощь по работе с ботом\n\n' \
           '⦁ Чтобы узнать цену валюты введите команду в формате:\n' \
           '  <имя_валюты> <в какую перевести> <количество>\n\n' \
           '  Пример:     доллар рубль 1\n\n' \
           '⦁ Узнать список доступных валют по команде: /values\n' \
           '⦁ Также можно ввести: "валюты", "список", "лист".'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values', 'валюты', 'список', 'лист'])
def list_currencies(message: telebot.types.Message):
    text = '🏦 Доступные валюты:\n'
    for key in currency.keys():
        text = '\n - '.join((text,  key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split()

    if values[0] in ['старт', 'помощь', 'хелп']:
        return helps(message)
    if values[0] in ['валюты', 'список', 'лист']:
        return list_currencies(message)

    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        if len(values) < 3:
            raise APIException('Недостаточно параметров.')
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'⚠ Ошибка при вводе команды:\n- {e}')
    except Exception as e:
        bot.reply_to(message, f'⚠ Не удалось обработать команду:\n{e}')
    else:
        at = amount.replace(',', '.')
        z1, z2 = currency[base][1], currency[quote][1]
        text = f'🏦 {base} ➔ {quote}\n💰 {at} ≈ ' \
               f'{round(float(total_base) * float(at), 2)} {z2}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
