import telebot
from telebot import types
import Cian_2
from time import sleep, strftime
from time import strftime
import DomoFond

bot = telebot.TeleBot('5324509616:AAE4_hmcPm3U_q4z-Am_VRsniQ_VF8XnAOo')

@bot.message_handler(commands=['start'])
def start(message):
    start_button = types.KeyboardButton(text='Циан')
    start_button_2 = types.KeyboardButton(text='DomoFond')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button, start_button_2)
    sent = bot.send_message(message.chat.id, 'Добро пожаловать', reply_markup=keyboard)
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
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так', )



"""_________________________Cian_______________________________"""
lists = []
@bot.message_handler(content_types=['text'])
def callback_workers(message):
        f = message.text
        lists.append(f)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы')
        bot.register_next_step_handler(qqq, callback__two)

def callback__two(message):
    page = message.text
    lists.append(page)
    Cian_2.main(ade=lists[0], pages=lists[1])
    timestr = strftime("%Y.%m.%d-%H.%M")
    doc = open(timestr + '_cian' + '.csv', 'rb')
    bot.send_document(message.chat.id, doc)

"""_________________________Domofond_______________________________"""

lists_DomoFond = []
@bot.message_handler(content_types=['text'])
def callback_workers_DomoFond(message):
        f = message.text
        print(f)
        lists_DomoFond.append(f)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы Домофонд')
        bot.register_next_step_handler(qqq, callback__two_DomoFond)


def callback__two_DomoFond(message):
    page = message.text
    print(page)
    lists_DomoFond.append(page)
    DomoFond.main(ade=lists_DomoFond[0], pages=lists_DomoFond[1])
    timestr = strftime("%Y.%m.%d-%H.%M")
    doc = open(timestr + '_Domofond' + '.csv', 'rb')
    bot.send_document(message.chat.id, doc)

if __name__ == '__main__':
    print('Online')
    bot.polling()

