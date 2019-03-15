import os
import random
from pprint import pprint

from pybooru import Danbooru
import telebot

import requests

UPLOAD_PATH = os.path.join('.', 'upload')
PHOTOS_PATH = os.path.join('.', 'photos')


token = '669924981:AAHdpsCv_YbA0nlpVjkw4acdMVAGTWYlNJI'
bot = telebot.TeleBot(token)


# На вход даем путь, из которого будет выбран случайный файл
# На выходе получаем путь содержимое случайного файла
def get_random_file(path):
    random.seed(os.urandom(128))
    file_list = os.listdir(path)
    random_file = random.choice(file_list)
    file_path = os.path.join(path, random_file)
    file_content = open(file_path, 'rb')
    return file_content


def get_random_photo():
    photo = get_random_file(PHOTOS_PATH)
    return photo


def generate_new_filename(file_path):
    filename = os.path.split(file_path)[1]
    file_extension = os.path.splitext(filename)[1]
    
    random.seed()
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    new_filename = ''.join(random.sample(alphabet, 16)) + file_extension

    return new_filename

def log_user_message(message):
    chat_logger_id = -268796265
    bot.send_message(chat_logger_id, '<b>' + message.from_user.username + '</b> sent <b>' + message.text + '</b>', parse_mode='html')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_user_message(message)
    welcome_message = 'Дружок-пирожок, тобой выбрана неправильная дверь. Клуб кожевенного ремесла двумя этажами ниже.'
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['findByTag'])
def send_found_photos(message):
    msg_args = message.text.split(' ')

    POST_PER_REQUEST = 200

    bot.send_message(message.chat.id, 'Начинаю...')

    tag_names = msg_args[1]
    client = Danbooru('danbooru')
    total_posts = client.tag_list(name=tag_names)[0]['post_count']

    pages_found = (total_posts // POST_PER_REQUEST) + 1
    params = {
        'limit': total_posts,
        'tags': tag_names,
        'page': None
    }
    for page in range(1, pages_found + 1):
        params['page'] = page
        founded_posts = client.post_list(**params)
        for post in founded_posts:
            if not 'file_url' in post.keys():
                continue
            file_url = post['file_url']
            response = requests.get(file_url)
            file_content = response.content
            bot.send_photo(message.chat.id, file_content)



@bot.message_handler(commands=['photo'])
def send_one_random_photo(message):
    log_user_message(message)
    bot.send_photo(message.chat.id, get_random_photo())


@bot.message_handler(commands=['photos'])
def send_several_random_photos(message):
    log_user_message(message)
    msg_args = message.text.split(' ')
    total_photos = 5

    if len(msg_args) != 1:
        try:
            total_photos = int(msg_args[1])
            if total_photos < 2:
                total_photos = 1
            if total_photos > 10:
                bot.send_message(message.chat.id, 'Ошибка! Нельзя запрашивать больше 10 изображений за раз')
                return
        except ValueError:
            bot.send_message(message.chat.id, 'Ошибка! Второй аргумент команды должен быть числом')
            return

    bot.send_message(message.chat.id, 'Фоток запрошено: {}'.format(total_photos))
    for i in range(total_photos):
        bot.send_photo(message.chat.id, get_random_photo())

@bot.message_handler(content_types=['document'])
def upload_file_to_temp(message):
    # photos = message.photo
    # total_photos = len(photos)
    # photo = message.photo[ total_photos - 1 ]
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    new_name = generate_new_filename(file_info.file_path)

    fullpath = os.path.join(UPLOAD_PATH, new_name)

    try:
        with open(fullpath, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Файл загружен на модерацию')
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка:\n' + e)

    # print(file_info)
    # uploaded_file = message.document
    # uploaded_filename = uploaded_file.
    # new_name = generate_new_filename(file_info.file_path)

@bot.message_handler(func=lambda m: True)
def just_log(message):
    log_user_message(message)

bot.polling()