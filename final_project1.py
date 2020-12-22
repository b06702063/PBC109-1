# _*_coding:utf8_*_

import requests
from bs4 import BeautifulSoup

enter_name = input('請輸入食材:')  # 食材種類
url = 'https://online.carrefour.com.tw/tw/search?key='  # 抓網址
url += enter_name
url += '&categoryId='
r = requests.get(url)  # 把網頁的原始碼抓下來
soup = BeautifulSoup(r.text, 'html.parser')


attr = {'type': "text/javascript"}
# 找到<script type = text/javascript>這個標籤
product_tags = soup.find_all('script', attrs=attr)

useful_inf = str(product_tags[12]).split(
    ',')  # 我研究完家樂福的網頁原始碼，發現需要的訊息是在第13個標籤裡，存成列表

product = []
price = []

name = ()
for i in useful_inf:
    if 'EecProductName' in i:  # 這個後面是品項名，所以我要找出列表中含EecProductName的
        name = i.strip('\\"')  # 把頭尾雜雜的字元去掉
        name = name.strip('EecProductName\\":\\"')  # 去掉這串字
        product.append(name)  # 存成品項名字的列表
for i in useful_inf:
    if 'RealPrice' in i:
        name = i.strip('\\"')
        name = name.strip('RealPrice\\":\\"')
        price.append(int(name))

product_price = zip(product, price)
print(dict(product_price))


'''costco'''

cos_url = 'https://www.costco.com.tw/search?text='  # 抓網址
cos_url += enter_name
cos_r = requests.get(cos_url)  # 抓下原始碼
cos_soup = BeautifulSoup(cos_r.text, 'html.parser')

cos_product = cos_soup.find_all('script', attrs=attr)

cos_useful = str(cos_product[3]).split(';')

cos_product_list = []
cos_price_list = []

for i in cos_useful:
    if 'gtm_products' in i:
        i.strip()
        print(i)
'''商品資訊存在gtm_products的list中'''
