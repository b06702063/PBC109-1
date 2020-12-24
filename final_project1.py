# _*_coding:utf8_*_
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

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

cos_useful = str(cos_product[3]).split('[')  # 資料位於第三塊

cos_product_list = []  # 用於記錄產品名
cos_price_list = []  # 用於紀錄價格

# 商品資訊存在gtm_products的list中

for i in cos_useful:
    if '"name"' in i:
        right = i.find(']')  # 選出包括右括號的字串
        i = i[:right]  # 切割字串
        cos_gtm = i.split('}')  # 網頁上產品串

cos_gtm.pop()  # list最後有空字串

for i in cos_gtm:
    for j in range(len(i)):
        if i[j-9: j] == '{"name":"':  # 找出商品名稱
            name_comma = i.find('"', j)
            cos_product_list.append(i[j:name_comma])
        if i[j-9: j] == '"price":"':  # 找出商品價格
            price_comma = i.find('"', j-1)
            cos_price_list.append(i[j:price_comma])

cos_product_price = zip(cos_product_list, cos_price_list)

print(dict(cos_product_price))


'''測試網站模擬器'''

opt = Options()
opt.add_argument('--disable-notifications')


chrome = webdriver.Chrome(
    executable_path=r"D:\\coding\\chromedriver.exe", chrome_options=opt)

chrome.get(url)

time.sleep(5)
