import time
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
from selectolax.parser import HTMLParser
import json



headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding": "gzip, deflate, br",
      "DNT": "1",
      "Connection": "keep-alive",
      "Cookie": "u=2taptwf8.1gciv6e.17r4q91p5skw; v=1651559500; luri=rossiya; buyer_location_id=621540; sx=H4sIAAAAAAAC%2F1TOQa6jMAwA0LtkzSKOYzvpbYKDA%2F10oBVFdCruPquOfi%2Fw9N4OisSqiF5CxNSjrwRVMVMoORB6d3m73V3cTDsAGtUhHHWVCWQ%2BxtfVfm5%2FZYwv17nBXYAJOFImOTuHJekwgHrwSSkmkxhRJYWsFgzzR%2B7Njr3ND6%2Fb7HUckVbeNrn7es%2By4G%2BZPfizc2Lsew2aGUoxClKlN%2FWWIBpx%2Bn%2B2%2Fc%2FyhBvpY7Zxam3nBbUtKlfUqfTfZ4Gzcxb7bCRS%2BljFF66ZbUgMwAYhBfnId94b5rxOz4ZXWdtP5o1Lm9Jy0ID7t%2Bz9ef4LAAD%2F%2F2ce%2B2VpAQAA; dfp_group=10; abp=1; SEARCH_HISTORY_IDS=4; _gcl_au=1.1.1401383401.1651559496; _ga_9E363E7BES=GS1.1.1651559495.1.1.1651559600.18; _ga=GA1.1.1377320955.1651559496; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b0df103df0c26013a84dcacfe8ebe897bfa4d7ea84258c63d59c9621b2c0fa58f164b09365f5308e7ad09145d3e31a56934d62295fceb188db5b87f59517a23f23de19da9ed218fe287829363e2d856a2e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe2d50b96489ab264ed3de19da9ed218fe23de19da9ed218fe246b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c84df0fd22b85d35f9230d9f49c8f2c8003f2e1a870b7803b8577330086cfc737f9d694871fd850cbe6b4ddffebbeebad28c8cb20c0b1c64521373224a87538e891e52da22a560f550df103df0c26013a0df103df0c26013aaaa2b79c1ae925950cff85276863ed9fa91940a5dfdfab063de19da9ed218fe22c205742455dd3668a7ab30b906d7a78; ft=hQBVMSZrXaLb96AkPHMAMEYcWBuv9fdadWZ0cr0H1lSZDzbP1htuDkLPuwLxS1Lk8RoT6YPK4CQjfe9F8/nnVaQV+Op88cILiwzvsfFnazjjehmWbRrZsl0IrzVyr/vdLD6ioaJp5AEY1dFhwtw6ACNXPzAo5yAjQ63nV8dO1s/GdlealbA7nibd1p6F614p"
         }

def get_html(url, retry=5):
    time.sleep(5)
    try:
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
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

def write_csv(data):
    timestr = time.strftime("%Y.%m.%d-%H.%M")
    with open(timestr + '_YaNed' + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['url'], data['price'], data['addres'], data['square'], data['advertisement']))

url_offer_numburs = []     
def get_page_data(html):
        tree = HTMLParser(html)
        script = tree.css_first('script[id="initial_state_script"]').text()
        script = script[23:-1]

        data = json.loads(script)
        with open('qqqq.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        print(data)
        offers = data['map']['offers']['points']
        for offer in offers:
             url_offer = offer['unsignedInternalUrl']
             url_offer_num = offer['unsignedInternalUrl'].split('/')[-1]
             url_offer_numburs.append(url_offer_num)
             creaor_date = offer['creationDate']
             area = offer['area']['value']
             price = offer['price']['value']
             address = offer['location']['geocoderAddress']
             # for i in url_offer_numburs:
             #      glav_url = f'https://realty.yandex.ru/gate/phone-modal/offer/?id={i}&rgid=300632&offerSiteId=2226687&crc=y2ded28937c6749e62ef37a28c680daf6&powB64=eyJoYXNoIjoiMDAwMDAxODBiZWE2ZTg0ZTJjYTllZWM1ZDk0ZGI2OTciLCJ0aW1lc3RhbXAiOjE2NTI0NjYwNTI0ODAsInBheWxvYWQiOiI1MjI2ODI1MzA0MzQ0NTUzNDQ3IiwidGltZVRvQ29tcGxldGUiOjQ2NX0%3D'
             #      res = requests.get(glav_url, headers=headers)
             #      game_result = res.json()
             #      phone = game_result['response']['phones']
             #data_offers = {'url': url_offer,  'price': price, 'addres': address, 'square': area, 'advertisement': creaor_date}

             #write_csv(data_offers)


def make_all(url):
    html = get_html(url)
    get_page_data(html)

def main():
    url = 'https://realty.yandex.ru/moskva/kupit/kvartira/?page={}'
    urls = [url.format(str(i)) for i in range(1, 2)]

    with Pool(1) as p:
        p.map(make_all, urls)


if __name__ == '__main__':
    main()