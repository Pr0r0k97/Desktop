import csv
import os
import re
from multiprocessing import Pool
from time import sleep, strftime

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By

import main


class Parsing():
    def __init__(self, ade, pages, user, id):
        self.id = id
        self.link = str(ade)
        self.page = int(pages)
        self.user = user
        text = re.sub(r'Page=\d+', 'Page={}', self.link)
        urls = [text.format(str(i)) for i in range(1, self.page)]
        with Pool(3) as p:
            p.map_async(self.get_page_data, urls)
            p.close()
            p.join()

    def get_page_data(self, url):
        count = 0
        for i in url:
            count += 1
            sleep(0.2)
        print(f'Выполняется парсинг {i} страниц из {self.page - 1}')
        main.info_DomoFond(one=i, two=self.page, id=self.id)
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        p = os.path.abspath('geckodriver.exe')
        driver = webdriver.Firefox(options=options, executable_path=p)
        driver.get(url=url)
        sleep(2)
        html = driver.page_source
        soup = BS(html, 'lxml')
        try:
            dates = soup.find('span', class_='long-item-card__listDate___1AWok').text
        except:
            dates = ''
        ads = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a',
                                                                                       class_='long-item-card__item___ubItG')
        for ad in ads:
            urls = 'https://www.domofond.ru' + ad.get('href')
            try:
                data_dobavlenia = ad.find('div', class_='long-item-card__informationFooterRight___3Xw4i').text
            except:
                data_dobavlenia = ''
            driver.get(urls)
            sleep(2)
            try:
                phone = driver.find_element(By.CLASS_NAME, 'button__button___3990j')
                phone.click()
            except:
                phone = ''
            sleep(2)
            htmls = driver.page_source
            soups = BS(htmls, 'lxml')
            try:
                name = soups.find('h1', class_='information__title___1nM29').text
            except:
                name = ''
            try:
                price = soups.find('div', class_='information__price___2Lpc0').text
            except:
                price = ''
            try:
                hous_kompleks = soups.find('a', class_='information__link___3UoKj').text
            except:
                hous_kompleks = ''
            try:
                addres = soups.find('a', class_='information__address___1ZM6d').text
            except:
                addres = ''
            try:
                metro = soups.find('div', class_='information__metro___2zFqN').text.split('M')[-1]
            except:
                metro = ''
            try:
                numbers = soups.find('a', class_='show-number-button__link___lB7O7').text
            except:
                numbers = ''

            data = {
                'dates': dates,
                'name': name,
                'price': price,
                'hous_kompleks': hous_kompleks,
                'addres': addres,
                'metro': metro,
                'numbers': numbers,
                'data_dobavlenia': data_dobavlenia
            }
            print(data)
            self.write_csv(data)

        # Сохранение в csv фаил

    def write_csv(self, data):
        timestr = strftime("%Y.%m.%d")
        with open(timestr + '_Domofond_' + self.user + '.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((data['name'], data['dates'], data['price'], data['hous_kompleks'], data['addres'],
                             data['metro'], data['numbers'], data['data_dobavlenia'], data['categor']))

    def end_func(self, response):
        print("Задание завершено")
