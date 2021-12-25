import requests
from telethon import TelegramClient, events, Button
from bs4 import BeautifulSoup
from config import TOKEN, API_ID, API_HASH

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)

def get_poem(address: str = '') -> str:
    url = f'http://perashki.ru{address}'
    r = requests.get(url).text
    
    soup = BeautifulSoup(r, 'lxml')
    result = soup.find('div', class_='Text').text
    author = soup.find('div', class_='Author').find('a').text
    date = soup.find('span', class_='date').text
    return f'''{result}
    Автор: {author:10}
    Дата публикации: {date}'''


@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await bot.send_message(
        event.peer_id.user_id,
        f'''Бот присылает случайное четверостишие - "пирожок" с сайта perashki.ru.
    Используй кнопки для взаимодействия с ботом.
    Случайный пирожок - стих из раздела "Рандом" сайта.
    Отборный пирожок - стих из раздела "Наше лучшее".
    Источник пирожков - ссылка на сайт perashki.ru''',
        buttons=[[Button.text('Случайный пирожок', resize=True), Button.text('Отборный пирожок', resize=True)],
                 [Button.text('Источник пирожков', resize=True)]]
    )


@bot.on(events.NewMessage)
async def main(event):
    msg = event.text
    user_id = event.peer_id.user_id
    if msg == '/help':
        await bot.send_message(user_id, 'Используй кнопки для взаимодействия с ботом')
    elif msg == 'Случайный пирожок':
        await bot.send_message(user_id, get_poem('/Piro/Random/'))
    elif msg == 'Отборный пирожок':
        await bot.send_message(user_id, get_poem())
    elif msg == 'Источник пирожков':
        await bot.send_message(user_id, 'perashki.ru')
bot.run_until_disconnected()

