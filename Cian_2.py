import os.path
import requests
import xlsxwriter
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import re
import time
from fake_useragent import UserAgent
from main import info_Cian
import xlsxwriter
import pandas


ua = UserAgent()

headers = {
     "User-Agent": ua.firefox,
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "DNT": "1",
      "Connection": "keep-alive",
       "Cookie": "_CIAN_GK=ca14318e-34ad-4246-b520-8cd5feae6cac; session_region_id=1; session_main_town_region_id=1; adb=1; sopr_utm=%7B%22utm_source%22%3A+%22kwork.ru%22%2C+%22utm_medium%22%3A+%22referral%22%7D; _gcl_au=1.1.243468318.1654361935; uxfb_usertype=searcher; uxs_uid=9eae8e20-e427-11ec-914c-d7ad1976a7c3; serp_registration_trigger_popup=1; distance_calculating_onboarding_counter=3; __cf_bm=_ESf.3LOr5dtzmSsKTf5GuWF1LXewVMwRyAaDHrCpOU-1654371461-0-AV5TeQuyg+bIjiCJn3h7S/CO19oVgI9udM8WiBDHrXA4w2VMNiNpwRHZWYxIy2Hrf2uPGc+jWuRvEVKNEovFjS8=; sopr_session=66ebbc8b599f4364"
}


def retrys(func, retries=5):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print("Пытаюсь восстановить подключение!")
                time.sleep(10)
                attempts += 1

    return retry_wrapper


# Делаем запрос к странице
@retrys
def get_html(url, retry=5):
    try:
        r = requests.get(url, headers=headers)
        #print(f"[+]  {url} {r.status_code}")
        print(f'Выполняется парсинг данной страницы {url}')
        info_Cian(one=url)
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
def write_csv(data, user):
    timestr = time.strftime("%Y.%m.%d")
    with open(timestr + '_cians_' + user + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['urls_info_block'], data['views'], data['data_dobavlenia'], data['addres'], data['price'], data['metro'], data['istoc'], data['peshkom'], data['kvdrat'], data['id_user'], data['url']))
    # xlsx_path = os.path.dirname(__file__) + r"\test.xlsx"
    # with pandas.ExcelWriter(timestr + '_cians_' + user + '.xlsx',mode="a" if os.path.exists(timestr + '_cians_' + user + '.xlsx') else "w") as wb:
    #     data.to_excel(wb, sheet_name='Summary', index=False)








# Ищем данные
def get_page_data(html, user):
    url_list = []
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='_93444fe79c--wrapper--W0WqH').find_all('article', class_='_93444fe79c--container--Povoi')
    for ad in ads:
        try:

            try:
                kom = ad.find('div', class_='_93444fe79c--subtitle--vHiOV').text.split()[0]
            except:
                kom = ''
            try:
                id_user = ad.find('span', class_='_93444fe79c--color_current_color--gpi6p').text
            except:
                id_user = ''
            try:
                kvadrat_metr = ad.find('div', class_='_93444fe79c--subtitle--vHiOV').text.split(' ')[2]
            except:
                kvadrat_metr = ''
            try:
                etazh = ad.find('div', class_='_93444fe79c--subtitle--vHiOV').text.split(' ')[-2]
            except:
                etazh = ''
            try:
                urls = ad.find('a', class_='_93444fe79c--link--eoxce').get('href')
                url_list.append(urls)
            except:
                urls = ''
            try:
                addres = ad.find('div', class_='_93444fe79c--labels--L8WyJ').text
            except:
                addres = ''

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
        for url in url_list:
            r = requests.get(url=url, headers=headers)
            try:
                soup = BeautifulSoup(r.text, 'lxml')
                urls_info_block = soup.find('div', class_='a10a3f92e9--print_phones--himoo').text
                try:
                    name = soup.find('h1', class_='a10a3f92e9--title--UEAG3').text
                except:
                    name = ''
                try:
                    price = soup.find('span', class_='a10a3f92e9--price_value--lqIK0').text
                except:
                    price = ''
                try:
                    views = soup.find('a', class_='a10a3f92e9--link--ulbh5').text
                except:
                    views = ''
                try:
                    data_dobavlenia = soup.find('div', class_='a10a3f92e9--container--DUOig').text
                except:
                    data_dobavlenia = ''
            except Exception as ex:
                print("Что-то пошло не так")

        data = {
                'name': name,
                'url': urls,
                'addres': addres,
                'price': price,
                'metro': metro,
                'istoc': istoc,
                'peshkom': peshkom,
                'kvdrat': kvdrat,
                'kom': kom,
                'kvadrat_metr': kvadrat_metr,
                'etazh': etazh,
                'urls_info_block': urls_info_block,
                'views': views,
                'data_dobavlenia': data_dobavlenia,
                'id_user': id_user
                }
        # data = pandas.DataFrame({
        #         'name': [name],
        #         'url': [urls],
        #         'addres': [addres],
        #         'price': [price],
        #         'metro': [metro],
        #         'istoc': [istoc],
        #         'peshkom': [peshkom],
        #         'kvadrat_metr': [kvadrat_metr],
        #         'urls_info_block': [urls_info_block],
        #         'views': [views],
        #         'data_dobavlenia': [data_dobavlenia],
        #         'id_user': [id_user]
        #         })
        print(data)
        write_csv(data, user)

def end_func(response):
    print("Задание завершено")


def make_all(url, user):
    for i in url:
        html = get_html(i)
    print(i)
    get_page_data(html, user)


def main(ade, pages, user):
    urlst = str(ade)
    page = int(pages)
    text = re.sub(r'p=\d+', 'p={}', urlst)
    urls = [text.format(str(i)) for i in range(1, page)]

    # Подключаем мультипроцессинг
    with Pool(4) as p:
        p.apply_async(make_all, args=(urls, user), callback=end_func)
        p.close()
        p.join()

if __name__ == '__main__':
    main()

