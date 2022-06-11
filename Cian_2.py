import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, Process
import re
import time
import main

headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "DNT": "1",
      "Connection": "keep-alive",
       "Cookie": "_CIAN_GK=7eb49d76-5a7e-49ec-b1f1-44097923c292; session_region_id=1; session_main_town_region_id=1; adb=1; sopr_utm=%7B%22utm_source%22%3A+%22kwork.ru%22%2C+%22utm_medium%22%3A+%22referral%22%7D; uxfb_usertype=searcher; uxs_uid=a24c5860-dba2-11ec-9511-6db685ddd7d2; serp_registration_trigger_popup=1; cookie_agreement_accepted=1; __cf_bm=sW4gQgPi6ZMFwEiD8DiUMRTdmNwfXHN_C0T3j0TO9pA-1653499426-0-AWkaQDF7t3uSzqfGg66fRcmmpecnwp0AoExDwUxdC+ISa1RYc4CpNelo2QJDKiaUkfVuNMS/Vmk1Ii7M5DGis1k=; _gcl_au=1.1.270258717.1653495045; sopr_session=95746daceb5a4e9f"
         }

# Делаем запрос к странице
def get_html(url, retry=5):
    time.sleep(5)
    try:
        r = requests.get(url, headers=headers)
        print(f"[+] {url} {r.status_code}")
    except Exception as ex:
        time.sleep(5)
        if retry:
            print(f"INFO retry={retry} => {url}")
            return get_html(url, retry=(retry - 1))
        else:
            raise
    else:
        return r.text


# Сохранение в csv фаил
def write_csv(data):
    timestr = time.strftime("%Y.%m.%d-%H.%M")
    with open(timestr + '_cian' + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['kom'], data['addres'], data['price'], data['metro'], data['istoc'], data['peshkom'], data['kvdrat'], data['url'], data['data_time']))


# Ищем данные
def get_page_data(html):

    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='_93444fe79c--wrapper--W0WqH').find_all('article', class_='_93444fe79c--container--Povoi')

    for ad in ads:
        # try:
        #     title = ad.find('div', class_='_93444fe79c--subtitle--vHiOV').text
        # except:
        #     title = ''
        try:
            try:
                kom = ad.find('span', class_='_93444fe79c--color_primary_100--mNATk').text
            except:
                kom = ''
            try:
                data_time = ad.find('div', class_='_93444fe79c--absolute--yut0v').text
            except:
                data_time = ''
            try:
                urls = ad.find('a', class_='_93444fe79c--link--eoxce').get('href')
                #url_list.append(urls)
            except:
                urls = ''
            try:
                addres = ad.find('div', class_='_93444fe79c--labels--L8WyJ').text
            except:
                addres = ''
            try:
                price = ad.find('span', class_='_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_28px--whmWV _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_22px--viEqA _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6').text.strip()
            except:
                price = ''
            try:
                metro = ad.find('a', class_='_93444fe79c--link--BwwJO').text
            except:
                metro = ''
            try:
                istoc = ad.find('a', class_='_93444fe79c--jk--dIktL').text
            except:
                istoc = ''
            try:
                peshkom = ad.find('div', class_='_93444fe79c--remoteness--q8IXp').text
            except:
                peshkom = ''
            try:
                kvdrat = ad.find('p', class_='_93444fe79c--color_gray60_100--MlpSF _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_normal--P9Ylg _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6').text
            except:
                kvdrat = ''
        except Exception as ex:
            continue

        data = {
                'url': urls,
                'addres': addres,
                'price': price,
                'metro': metro,
                'istoc': istoc,
                'peshkom': peshkom,
                'kvdrat': kvdrat,
                'kom': kom,
                'data_time': data_time
                }

        write_csv(data)


def make_all(url):
    html = get_html(url)
    get_page_data(html)




def main(ade, pages):
    urlst = str(ade)
    page = int(pages)
    text = re.sub(r'p=\d', 'p={}', urlst)
    urls = [text.format(str(i)) for i in range(1, page)]


    #Подключаем мультипроцессинг
    # with Pool(10) as p:
    #     p.map(make_all, urls)



if __name__ == '__main__':
    main()