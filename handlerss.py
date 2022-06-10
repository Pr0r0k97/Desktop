from main import *
import Cian_2
import time



lists = []
@bot.message_handler(content_types=['text'])
def callback_workers(message):
        f = message.text
        lists.append(f)
        print(lists)
        qqq = bot.send_message(message.chat.id, 'Введите номер страницы')
        bot.register_next_step_handler(qqq, callback__two)


def callback__two(message):
    page = message.text
    lists.append(page)
    print(page)
    Cian_2.main(ade=lists[0], pages=lists[1])
    timestr = time.strftime("%Y.%m.%d-%H.%M")
    doc = open(timestr + '_cian' + '.csv', 'rb')
    bot.send_document(message.chat.id, doc)