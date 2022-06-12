import telebot
from telebot import types
import Cian_2
from time import strftime
import DomClik
import DomoFond
import re

bot = telebot.TeleBot('5324509616:AAE4_hmcPm3U_q4z-Am_VRsniQ_VF8XnAOo')
global list_name
list_name = []

@bot.message_handler(commands=['start'])
def start(message):
    start_button = types.KeyboardButton(text='Циан')
    start_button_2 = types.KeyboardButton(text='DomoFond')
    start_button_3 = types.KeyboardButton(text='DomClick')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button, start_button_2, start_button_3)
    user_first_name = str(message.chat.first_name)
    list_name.append(user_first_name)
    sent = bot.send_message(message.chat.id, f'Добро пожаловать {user_first_name}',  reply_markup=keyboard)
    bot.register_next_step_handler(sent, callback_worker)



def callback_worker(message):
    if message.text == 'Циан':
        qs = bot.send_message(message.chat.id, 'Введите ссылку')
        if qs:
            bot.register_next_step_handler(qs, callback_workers)
    elif message.text == 'DomoFond':
        qe = bot.send_message(message.chat.id, 'Введите ссылку DomoFond')
        if qe:
            bot.register_next_step_handler(qe, callback_workers_DomoFond)
    elif message.text == 'DomClick':
        qe = bot.send_message(message.chat.id, 'Введите ссылку DomClick')
        if qe:
            bot.register_next_step_handler(qe, callback_workers_DomClick)
    else:
        bot.send_message(message.chat.id, 'Выберете кнопку', )



"""_________________________Cian_______________________________"""
lists = []

def callback_workers(message):
        f = message.text
        if 'https://' in f:
            lists.append(f)
            qqq = bot.send_message(message.chat.id, 'Введите номер страницы')
            bot.register_next_step_handler(qqq, callback__two)
        else:
            bot.send_message(message.chat.id, 'Введите \start и начните все сначало')

def callback__two(message):
    page = message.text
    if re.search('\d+', page):
        lists.append(page)
        user_first_name = str(message.chat.first_name)
        Cian_2.main(ade=lists[0], pages=lists[1], user=user_first_name)
        # timestr = strftime("%Y.%m.%d-%H.%M")
        # doc = open(timestr + '_cian' + '.csv', 'rb')
        # bot.send_document(message.chat.id, doc)
    else:
        bot.send_message(message.chat.id, 'Введите \start и начните все сначало')


"""_________________________Domofond_______________________________"""

lists_DomoFond = []
def callback_workers_DomoFond(message):
        f = message.text
        if 'https://www.domofond.ru' in f:
            lists_DomoFond.append(f)
            qqq = bot.send_message(message.chat.id, 'Введите номер страницы Домофонд')
            bot.register_next_step_handler(qqq, callback__two_DomoFond)
        else:
            bot.send_message(message.chat.id, 'Введите \start и начните все сначало')


def callback__two_DomoFond(message):
        page = message.text
        print(page)
        if re.search('\d+', page):
            lists_DomoFond.append(page)
            DomoFond.main(ade=lists_DomoFond[0], pages=lists_DomoFond[1])
            timestr = strftime("%Y.%m.%d-%H.%M")
            doc = open(timestr + '_Domofond' + '.csv', 'rb')
            bot.send_document(message.chat.id, doc)
        else:
            bot.send_message(message.chat.id, 'Введите \start и начните все сначало')





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
            bot.send_message(message.chat.id, 'Введите \start и начните все сначало')

def callback__two_DomClick(message):
    page = message.text
    print(page)
    if re.search('\d+', page):
        lists_DomClick.append(page)
        DomClik.main(ade=lists_DomClick[0], pages=lists_DomClick[1])
        timestr = strftime("%Y.%m.%d-%H.%M")
        doc = open(timestr + '_DomClick' + '.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    else:
        bot.send_message(message.chat.id, 'Введите \start и начните все сначало')



@bot.message_handler(content_types=['text'])
def callback__two_Start(message):
    bot.send_message(message.chat.id, 'Нажмите старт заново')
    start




if __name__ == '__main__':
    print('Online')
    bot.polling()





