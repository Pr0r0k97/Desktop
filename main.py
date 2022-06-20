import logging
import re
import time
from time import strftime

import telebot
from telebot import types

import Cian_2
import DomClik
import DomoFond
import tg_analytic

bot = telebot.TeleBot('5582241891:AAGqYgrgB1dmjPpsQftQ7nvPQMoL2B3rOCk')


# Logger
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def start(message):
    start_button = types.KeyboardButton(text='💰 Циан')
    start_button_2 = types.KeyboardButton(text='💵 DomoFond')
    start_button_3 = types.KeyboardButton(text='🔥 DomClick')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button, start_button_2, start_button_3)
    user_first_name = str(message.chat.first_name)
    sent = bot.send_message(message.chat.id,
                            f'Добро пожаловать {user_first_name} 🔥\nТебя приветствует BotParserNedvizhimost\nИнструкция:\n1. Выбери кнопку сайта данные которого вы хотите спарсить\n2. Вставте ссылку ОБЯЗАТЕЛЬНО СО ВТОРОЙ СТРАНИЦЫ\n3. Введите количество страниц которое вы хотите спарсить!\n4. Среднее количество парсинга 1 страницы заимает 5-10 минут!',
                            reply_markup=keyboard)
    # video = open('Bot tutorial.mp4', 'rb')
    # bot.send_video(message.chat.id, video)
    bot.register_next_step_handler(sent, callback_worker)


def callback_worker(message):
    if message.text == '💰 Циан':
        qs = bot.send_message(message.chat.id, 'Введите ссылку')
        if qs:
            bot.register_next_step_handler(qs, callback_workers)
    elif message.text == '💵 DomoFond':
        qe = bot.send_message(message.chat.id, 'Введите ссылку DomoFond')
        if qe:
            bot.register_next_step_handler(qe, callback_workers_DomoFond)
    elif message.text == '🔥 DomClick':
        qe = bot.send_message(message.chat.id, 'Введите ссылку DomClick')
        if qe:
            bot.register_next_step_handler(qe, callback_workers_DomClick)
    elif message.text[:10] == 'статистика' or message.text[:10] == 'Cтатистика':
        st = message.text.split(' ')
        if 'txt' in st or 'тхт' in st:
            tg_analytic.analysis(st, message.chat.id)
            with open('%s.txt' % message.chat.id, 'r', encoding='UTF-8') as file:
                bot.send_document(message.chat.id, file)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(st, message.chat.id)
            bot.send_message(message.chat.id, messages)
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


"""_________________________Cian_______________________________"""

lists = []


def callback_workers(message):
    f = message.text
    if 'https://' in f:
        lists.append(f)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы')
        bot.register_next_step_handler(qqq, callback__two)
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def callback__two(message):
    page = message.text
    qwe = message.chat.id
    if re.search('\d+', page):
        lists.append(page)
        user_first_name = str(message.chat.first_name)
        Cian_2.main(ade=lists[0], pages=lists[1], user=user_first_name, id=qwe)
        timestr = strftime("%Y.%m.%d")
        doc = open(timestr + '_cians_' + user_first_name + '.csv', 'rb')
        bot.send_document(message.chat.id, doc)
        time.sleep(5)
        open(timestr + '_cians_' + user_first_name + '.csv', 'w').close()

    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def info_Cian(one, id):
    print(one)
    bot.send_message(chat_id=id, text=f'Cian: Выполняется парсинг данной страницы {one}')


"""_________________________Domofond_______________________________"""

lists_DomoFond = []


def callback_workers_DomoFond(message):
    f = message.text
    if 'https://www.domofond.ru' in f:
        lists_DomoFond.append(f)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы Домофонд')
        bot.register_next_step_handler(qqq, callback__two_DomoFond)
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def callback__two_DomoFond(message):
    page = message.text
    id = message.chat.id
    if re.search('\d+', page):
        lists_DomoFond.append(page)
        user_first_name = str(message.chat.first_name)
        DomoFond.Parsing(ade=lists_DomoFond[0], pages=lists_DomoFond[1], user=user_first_name, id=id)
        timestr = strftime("%Y.%m.%d")
        doc = open(timestr + '_Domofond_' + user_first_name + '.csv', 'rb')
        bot.send_document(message.chat.id, doc)
        time.sleep(5)
        open(timestr + '_Domofond_' + user_first_name + '.csv', 'w').close()
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def info_DomoFond(one, two, id):
    bot.send_message(chat_id=id, text=f'DomoFond: Выполняется парсинг {one} страниц из {two - 1}')


"""_________________________DomClick_______________________________"""

lists_DomClick = []


def callback_workers_DomClick(message):
    f = message.text
    print(f)
    if 'https://domclick.ru' in f:
        lists_DomClick.append(f)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы Домклик')
        bot.register_next_step_handler(qqq, callback__two_DomClick)
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def callback__two_DomClick(message):
    page = message.text
    id = message.chat.id
    if re.search('\d+', page):
        lists_DomClick.append(page)
        user_first_name = str(message.chat.first_name)
        DomClik.Parsing_Domclick(ade=lists_DomClick[0], pages=lists_DomClick[1], user=user_first_name, id=id)
        timestr = strftime("%Y.%m.%d")
        doc = open(timestr + '_DomClick' + '.csv', 'rb')
        bot.send_document(message.chat.id, doc)
        time.sleep(5)
        open(timestr + '_DomClick' + '.csv', 'w').close()
    else:
        bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')


def info_DomClick(one, two, id):
    bot.send_message(chat_id=id, text=f'DomClick: Выполняется парсинг {one} страниц из {two}')


# @bot.message_handler(content_types=['text'])
# def callback__two_Start(message):
#         bot.send_message(message.chat.id, 'Введите /start и начните все сначало 😉')
#         start

if __name__ == '__main__':
    # Polling
    while True:
        try:
            print('Online')
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(e)
            time.sleep(5)
