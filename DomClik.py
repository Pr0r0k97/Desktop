from time import sleep, strftime
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool
import re
import csv
from selenium import webdriver
import os
import time


class Parsing_Domclick():
    def __init__(self, ade, pages, user):
        self.link = str(ade)
        self.page = int(pages)
        self.user = user
        text = re.sub(r'page=\d+', 'page={}', self.link)
        urls = [text.format(str(i)) for i in range(1, self.page)]

        with Pool(3) as p:
            p.map(self.get_page_data, urls)

    # #Сохранение в csv фаил
    def write_csv(self, data):
        timestr = strftime("%Y.%m.%d")
        with open(timestr + '_DomClick_' + self.user + '.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((data['name'], data['numbers'], data['price'], data['views'], data['data_dobavlenia'], data['metro'], data['addres'], data['kvdrat_metr'], data['name_user']))


    def get_page_data(self, url):
        count = 0
        for i in url:
            count += 1
        print(f'Выполняется парсинг {i} страницы из {self.page}')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized");
        p = os.path.abspath('chromedriver.exe')
        driver = webdriver.Chrome(chrome_options=options, executable_path=p)
        driver.get('https://nova.rambler.ru/search?utm_source=head&utm_campaign=self_promo&utm_medium=form&utm_content=search&query=domclick')
        time.sleep(5)
        Button_email = driver.find_element(By.LINK_TEXT, 'domclick.ru')
        Button_email.click()
        time.sleep(5)

        driver.get(url=url)

        time.sleep(5)

        html = driver.page_source
        soup = BS(html, 'lxml')
        ads = soup.find('div', class_='o9A9H').find_all('div', class_='Kli35')
        for ad in ads:
            urlss = 'https://domclick.ru' + ad.find('a', class_='property_container__H4X9K').get('href')
            driver.get(url=urlss)
            sleep(5)
            phone = driver.find_element(By.CSS_SELECTOR, '.Kx0Q4 > button:nth-child(1)')
            phone.click()
            sleep(5)
            htmls = driver.page_source
            soups = BS(htmls, 'lxml')

            try:
                name = soups.find('h1', class_='Z0SoN').text
            except:
                name = ''
            try:
                numbers = soups.find('a', class_='button-root-8-1-2 button-root--primary-8-1-2 button-root--large-8-1-2 button-root--type-link-reset-8-1-2 button-root--fluid-8-1-2').text
            except:
                numbers = ''
            try:
                price = soups.find('div', class_='fsnok').text
            except:
                price = ''
            try:
                views = soups.find('span', class_='dM1Sl').text
            except:
                views = ''
            try:
                data_dobavlenia = soups.find('div', class_='hfJ0+').text
            except:
                data_dobavlenia = ''
            try:
                metro = soups.find('a', class_='_2Bq_F').text
            except:
                metro = ''
            try:
                addres = soups.find('span', class_='S8rOu').text
            except:
                addres = ''
            try:
                kvdrat_metr = soups.find('div', class_='dhZVF').text
            except:
                kvdrat_metr = ''
            try:
                name_user = soups.find('a', class_='O77Er').text
            except:
                name_user = ''
            data = {
                'name': name,
                'numbers': numbers,
                'price': price,
                'views': views,
                'data_dobavlenia': data_dobavlenia,
                'metro': metro,
                'addres': addres,
                'kvdrat_metr': kvdrat_metr,
                'name_user': name_user
            }
            print(data)
            self.write_csv(data)













