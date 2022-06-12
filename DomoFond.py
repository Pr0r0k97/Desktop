from selenium import webdriver
from time import sleep, strftime
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import  Options as  FirefoxOptions
from bs4 import BeautifulSoup as BS
import os
from multiprocessing import Pool
import re
import csv
import time


# Сохранение в csv фаил
def write_csv(data, user):
    timestr = strftime("%Y.%m.%d")
    with open(timestr + '_Domofond_' + user + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['dates'], data['price'], data['hous_kompleks'], data['addres'], data['metro'], data['numbers']))


def get_page_data(url, user):
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
    ads = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a', class_='long-item-card__item___ubItG')
    for ad in ads:
       urls = 'https://www.domofond.ru' + ad.get('href')
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
       try:
            categor = soups.find('div', class_='detail-information__wrapper___FRRqm').text
       except:
            categor = ''
       data = {
                'dates': dates,
                'name': name,
                'price': price,
                'hous_kompleks': hous_kompleks,
                'addres': addres,
                'metro': metro,
                'numbers': numbers,

                }
       print(data)
       write_csv(data)




def end_func(response):
    print("Задание завершено")


def main(ade, pages, user):
    link = str(ade)
    page = int(pages)
    text = re.sub(r'Page=\d+', 'Page={}', link)
    urls = [text.format(str(i)) for i in range(1, page)]
    with Pool(3) as p:
        p.apply_async(get_page_data, args=(urls, user), callback=end_func)
        p.close()
        p.join()



if __name__ == '__main__':
    main()




