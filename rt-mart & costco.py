# _*_coding:utf8_*_

# 大潤發的爬蟲

import requests
from bs4 import BeautifulSoup
import math

enter_name = input('請輸入商品:')  # 輸入商品

rtmart_url = 'https://www.rt-mart.com.tw/direct/index.php?action=prod_search&prod_keyword='  # 抓網址
rtmart_url += enter_name
rtmart_url += '&auto_date_start=&auto_date_end=&price_range=&price_range_top=&price_range_bottom=&prod_sort_uid=&p_data_num=30&usort=&page='
rtmart_content = requests.get(rtmart_url)
soup = BeautifulSoup(rtmart_content.text, 'html.parser')  # 爬網頁內容

# 這一段是在找頁數
attr = {'class': 't02'}
items_number = int(str(soup.find_all('span', attrs=attr)).replace(
    '<span class="t02">', '').replace('</span>', '').replace('[', '').replace(']', ''))  # 找到商品總共有幾項
page = math.ceil(items_number/30)  # 大潤發是一頁放30項，所以我就用商品數除一頁放幾項然後無條件進位，就是頁數了

# 開始找商品
product = []
price = []
for count in range(1, page+1):  # 然後把總共的頁數寫成迴圈

    url1 = rtmart_url + str(count)  # 把頁數加進網址

    r = requests.get(url1)
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')  # 再爬一次新的網頁內容

    # 我研究大潤發的網頁原始碼，發現需要的商品名稱和價格訊息是在第13個標籤裡
    product_name = soup.find_all('script')[12]
    useful_inf = str(product_name).split(',')  # 存成列表

    name = ()

    for i in useful_inf:
        if 'name' in i:  # 找出列表中含name的項目，後面有商品品名
            name = i.replace('{', '').replace('"', '').replace('name', '').replace(
                ':', '').replace('[', '').replace('impressions', '')  # 去掉雜質
            product.append(name)  # 存成品項名字的列表

    for i in useful_inf:
        if 'price' in i:
            name = i.replace('"', '').replace('price:', '')
            price.append(int(name))  # 存成品項價格的列表


product_price = dict(zip(product, price))  # 把品名和價格zip成dictionary
rtmart_sort_product_price = sorted(
    product_price.items(), key=lambda x: x[1], reverse=False)  # 就由價格小到大排列

# costco的爬蟲

costco_url = "https://www.costco.com.tw/search?text="  # 好市多網站
costco_url += enter_name
costco_content = requests.get(costco_url)
soup = BeautifulSoup(costco_content.text, "html.parser")  # html parser

attr = {'type': "text/javascript"}

products = soup.find_all("script", attrs=attr)
useful_inf = str(products[3]).split(',')

product = []
price = []
name = ()
for i in useful_inf:
    if 'name' in i:
        o = i.replace('"', '')
        s = o.find('name:')
        name = o[s+5:]
        product.append(name)
for i in useful_inf:
    if 'price' in i:
        name = ''.join([x for x in i if x.isdigit()])
        if name == '':
            pass
        else:
            price.append(int(name))

product.pop(0)  # 去除亂碼e
product.pop(0)  # 去除亂碼name


product_price = dict(zip(product, price))
print(product_price)

costco_sort_product_price = sorted(
    product_price.items(), key=lambda x: x[1], reverse=False)
print(product_price)
'''
print('------')
print('大潤發的最低價格的推薦是：')
print(rtmart_sort_product_price[0])
print(rtmart_sort_product_price[1])
print(rtmart_sort_product_price[2])  # 印出前三個便宜的
print('------')
print('costco的最低價格的推薦是：')
print(costco_sort_product_price[0])
print(costco_sort_product_price[1])
print(costco_sort_product_price[2])
'''
