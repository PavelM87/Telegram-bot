import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
from flask import Flask, request
from config import token, secret, my_url


url = my_url + secret

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)

app = Flask(__name__)

keyboard = types.ReplyKeyboardMarkup(True)
keyboard.row('Случайный пирожок','Отборный пирожок')
keyboard.row('Источник пирожков')

def get_random():
    url = 'http://perashki.ru/Piro/Random/'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    result = soup.find('div', class_='Text').text
    author = soup.find('div', class_='Author').find('a').text
    date = soup.find('span', class_='date').text
    return f'''{result}

    Автор: {author:10}
    Дата публикации: {date}'''

def get_best():
    url = 'http://perashki.ru'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    result = soup.find('div', class_='Text').text
    author = soup.find('div', class_='Author').find('a').text
    date = soup.find('span', class_='date').text
    return f'''{result}

    Автор: {author:10}
    Дата публикации: {date}'''

@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f'''Бот присылает случайное четверостишие - "пирожок" с сайта perashki.ru.
    Используй кнопки для взаимодействия с ботом.
    Случайный пирожок - четверостишие из раздела "Рандом" сайта.
    Отборный пирожок - четверостишие из раздела "Наше лучшее".
    Источник пирожков - ссылка на сайт perashki.ru''')
    send(m.chat.id, get_best())

@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, f'''Бот присылает случайное четверостишие - "пирожок" с сайта perashki.ru.
    Используй кнопки для взаимодействия с ботом.
    Случайный пирожок - четверостишие из раздела "Рандом" сайта.
    Отборный пирожок - четверостишие из раздела "Наше лучшее".
    Источник пирожков - ссылка на сайт perashki.ru''')

@bot.message_handler(content_types=['text'])
def main(message):
    id = message.chat.id
    msg = message.text
    if msg == 'Случайный пирожок':
        send(id, get_random())
    elif msg == 'Отборный пирожок':
        send(id, get_best())
    elif msg == 'Источник пирожков':
        send(id, 'perashki.ru')
    else:
        send(id, 'Используй кнопки!')



def send(id, text):
    bot.send_message(id, text, reply_markup=keyboard)

