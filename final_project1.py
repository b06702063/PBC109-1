# _*_coding:utf8_*_

import requests
from bs4 import BeautifulSoup

enter_name = input('請輸入食材:')
url = 'https://online.carrefour.com.tw/tw/search?key='  # 抓網址
url += enter_name
url += '&categoryId='
r = requests.get(url)  # 把網頁的原始碼抓下來
soup = BeautifulSoup(r.text, 'html.parser')


attr = {'type': "text/javascript"}
product_tags = soup.find_all('script', attrs=attr)

useful_inf = str(product_tags[12]).split(',')

product = []
price = []

name = ()
for i in useful_inf:
    if 'EecProductName' in i:
        name = i.strip('\\"')
        name = name.strip('EecProductName\\":\\"')
        product.append(name)
for i in useful_inf:
    if 'RealPrice' in i:
        name = i.strip('\\"')
        name = name.strip('RealPrice\\":\\"')
        price.append(int(name))

product_price = zip(product, price)
print(dict(product_price))

'''costco網站'''
cos_url = 'https://www.costco.com.tw/search?text='  # 抓網址
cos_url += enter_name

cos_r = requests.get(cos_url)  # 抓下原始碼
cos_soup = BeautifulSoup(cos_r.text, 'html.parser')


cos_product_tags = soup.find_all('script', attrs=attr)
