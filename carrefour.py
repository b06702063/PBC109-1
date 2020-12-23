# _*_coding:utf8_*_
  # 家樂福的爬蟲
import requests
from bs4 import BeautifulSoup
import json

product = []
price = []

enter_name = input('請輸入商品:')
url = 'https://online.carrefour.com.tw/tw/search?key='  # 抓網址
url += enter_name
url += '&categoryId='

r = requests.get(url)
content = r.text
soup = BeautifulSoup(content, 'html.parser')
attr = {'type':"text/javascript"}
product_tags = soup.find_all('script', attrs = attr)  # 找到<script type = text/javascript>這個標籤
useful_inf = str(product_tags[12]).split(',')  # 我研究完家樂福的網頁原始碼，發現需要的訊息是在第13個標籤裡，存成列表


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

product_price = dict(zip(product, price))
sort_product_price = sorted(product_price.items(), key = lambda x : x[1], reverse = False)


print('最低價格的推薦是：')
print(sort_product_price[0])
print(sort_product_price[1])
print(sort_product_price[2])
