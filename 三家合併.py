# _*_coding:utf8_*_

# 大潤發的爬蟲

import requests
from bs4 import BeautifulSoup
import math
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

while True:  # 用於程式重複執行
    enter_name = input('請輸入商品:')  # 輸入商品

    '''大潤發爬蟲'''
    rtmart_url = 'https://www.rt-mart.com.tw/direct/index.php?action=prod_search&prod_keyword='  # 抓網址
    rtmart_url += enter_name
    rtmart_url += '&auto_date_start=&auto_date_end=&price_range=&price_range_top=&price_range_bottom=&prod_sort_uid=&p_data_num=30&usort=&page='
    rtmart_content = requests.get(rtmart_url)
    soup = BeautifulSoup(rtmart_content.text, 'html.parser')  # 爬網頁內容

    # 這一段是在找頁數
    attr = {'class': 't02'}
    items_number = int(str(soup.find_all('span', attrs=attr)).replace(
        '<span class="t02">', '').replace('</span>', '').replace('[', '').replace(']', ''))  # 找到商品總共有幾項
    page = math.ceil(items_number/30)  # 大潤發是一頁放30項，用商品數除一頁放幾項並無條件進位，求出頁數

    # 開始找商品
    product = []  # 產品名稱
    price = []  # 產品價格
    for count in range(1, page+1):  # 總共的頁數寫成迴圈

        url1 = rtmart_url + str(count)  # 頁數加進網址

        r = requests.get(url1)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')  # 再爬一次新的網頁內容

        # 商品名稱與價格存在第13個區塊
        product_name = soup.find_all('script')[12]
        useful_inf = str(product_name).split(',')  # 存成列表

        name = ()  # 將名字存成tuple

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

    '''costco的爬蟲'''

    costco_url = "https://www.costco.com.tw/search?text="  # 好市多網站
    costco_url += enter_name
    costco_content = requests.get(costco_url)
    soup = BeautifulSoup(costco_content.text, "html.parser")  # html parser

    attr = {'type': "text/javascript"}

    products = soup.find_all("script", attrs=attr)  # 抓下網站資料
    useful_inf = str(products[3]).split(',')  # 資料位於第四個區塊

    product = []  # 產品名稱
    price = []  # 產品價格
    name = ()  # 將單一產品存成tuple

    for i in useful_inf:
        if '"price":' in i:  # costco商品價格存在"price"後
            # costco網站會出現有商品名而沒有價格的現象，需要排除
            name = ''.join([x for x in i if x.isdigit()])
            price.append(name)

    for i in useful_inf:
        if '"name":' in i:
            o = i.replace('"', '')  # 去除"符號
            s = o.find('name:')  # 商品名稱存在name後面
            name = o[s+5:]  # name:佔五個字元
            product.append(name)

    new_price = []
    new_product = []
    for i in range(len(price)):
        if price[i] == '':  # 避免因缺失商品價格而與商品名對應錯誤
            pass
        else:
            new_price.append(int(price[i]))  # 將文字轉為數字
            new_product.append(product[i])

    product_price = dict(zip(new_product, new_price))  # 組成dictionary

    costco_sort_product_price = sorted(
        product_price.items(), key=lambda x: x[1], reverse=False)  # 按價格排序

    '''家樂福爬蟲'''
    # 家樂福網站無法用換網址來換頁，所以使用了selenium套件來爬蟲
    # 使用selenium套件 開啟google chorme
    driver = webdriver.Chrome("D:\\coding\\chromedriver.exe")
    url = 'https://online.carrefour.com.tw/tw/search?key='  # 家樂福網址
    url += enter_name
    url += '&categoryId='
    driver.get(url)  # 開啟家樂福網站

    # 找出總共品項有多少個，以便知道需要換頁幾次
    total_items_list = driver.find_elements_by_class_name('control')
    total_items_number = float(total_items_list[0].text.strip(
        "筆資料\n最多人購買 價格↓ 上架時間↓").strip('搜尋“').strip(enter_name).strip('” 共"'))
    total_pages = int((total_items_number//24) + 1)

    # 把商品名稱與價錢找出來
    product = []
    price = []

    for i in range(total_pages):  # 迴圈跑需要換頁的次數
        item_list = driver.find_elements_by_class_name(  # 發現家樂福網站的商品名和價錢會放在一個class叫desc-operation-wrapper的裡面
            'desc-operation-wrapper')                    # 並利用find_elements_by_class_name找出存取商品名稱價錢的list
        for item in item_list:
            temp = item.text.split('\n')
            product.append(temp[0])                      # 把商品名append到list裡
            price.append(int(temp[-1].strip('$')))       # 把價錢append到list裡

        if total_pages >= 7:                             # 找到換頁按鈕的位置
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[10]')
        elif total_pages == 6:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[9]')
        elif total_pages == 5:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[8]')
        elif total_pages == 4:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[7]')
        elif total_pages == 3:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[6]')
        elif total_pages == 2:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[5]')
        elif total_pages == 1:
            next_button = driver.find_element_by_xpath(
                '//*[@id="pagination"]/li[4]')
        next_button.click()                             # 利用click按下換頁按鈕
        time.sleep(1)                                   # 利用sleep來閒置一下網站

    # 把商品名和價錢合在一起，並依價錢排序
    product_price = dict(zip(product, price))
    carefour_sort_product_price = sorted(
        product_price.items(), key=lambda x: x[1], reverse=False)

    print('------')  # 分隔線
    print('大潤發的最低價格的推薦是：')
    if len(rtmart_sort_product_price) == 0:  # 處理資料數少於三筆
        print('此項商品不存在')
    if len(rtmart_sort_product_price) == 1:
        print(rtmart_sort_product_price[0])
    elif len(rtmart_sort_product_price) == 2:
        print(rtmart_sort_product_price[0])
        print(rtmart_sort_product_price[1])
    elif len(rtmart_sort_product_price) > 2:
        print(rtmart_sort_product_price[0])
        print(rtmart_sort_product_price[1])
        print(rtmart_sort_product_price[2])

    print('------')
    print('costco的最低價格的推薦是：')
    if len(costco_sort_product_price) == 0:  # 處理資料數少於三筆
        print('此項商品不存在')
    if len(costco_sort_product_price) == 1:
        print(costco_sort_product_price[0])
    elif len(costco_sort_product_price) == 2:
        print(costco_sort_product_price[0])
        print(costco_sort_product_price[1])
    elif len(costco_sort_product_price) > 2:
        print(costco_sort_product_price[0])
        print(costco_sort_product_price[1])
        print(costco_sort_product_price[2])

    print('------')
    print('家樂福的最低價格的推薦是：')
    if len(carefour_sort_product_price) == 0:  # 處理資料筆數少於三筆
        print('此項商品不存在')
    if len(carefour_sort_product_price) == 1:
        print(carefour_sort_product_price[0])
    elif len(carefour_sort_product_price) == 2:
        print(carefour_sort_product_price[0])
        print(carefour_sort_product_price[1])
    elif len(carefour_sort_product_price) > 2:
        print(carefour_sort_product_price[0])
        print(carefour_sort_product_price[1])
        print(carefour_sort_product_price[2])
