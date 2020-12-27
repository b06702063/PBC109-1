import requests
from bs4 import BeautifulSoup
import math
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import tkinter as tk

root = tk.Tk()


class information(tk.Frame):

    global a, b, c

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.input_information()
        self.text=tk.StringVar()
        self.text.set("answer")

    def input_information(self):
        self.buscar = tk.Text(self, height=1, width=40)  # 5
        self.enter = tk.Button(self, text="Buscar", command=lambda: [self.searching(), self.changewords()])  # 1
        self.Block = tk.Label(self, text="answer")
        self.Block.grid(row=1, rowspan=5, columnspan=6)
        self.buscar.grid(row=0, column=0, columnspan=5)
        self.enter.grid(row=0, column=6)
        self.answer1 = tk.Label(self, text="none")
        self.answer2 = tk.Label(self, text="none")
        self.answer3 = tk.Label()


    def searching(self):
        enter_name = self.buscar.get("1.0", tk.END)
        rtmart_url = 'https://www.rt-mart.com.tw/direct/index.php?action=prod_search&prod_keyword='  # 抓網址
        rtmart_url += enter_name
        rtmart_url += '&auto_date_start=&auto_date_end=&price_range=&price_range_top=&price_range_bottom=&prod_sort_uid=&p_data_num=30&usort=&page='
        rtmart_content = requests.get(rtmart_url)
        soup = BeautifulSoup(rtmart_content.text, 'html.parser')  # 爬網頁內容

        # 這一段是在找頁數
        attr = {'class': 't02'}
        items_number = int(str(soup.find_all('span', attrs=attr)).replace(
            '<span class="t02">', '').replace('</span>', '').replace('[', '').replace(']', ''))  # 找到商品總共有幾項
        page = math.ceil(items_number / 30)  # 大潤發是一頁放30項，所以我就用商品數除一頁放幾項然後無條件進位，就是頁數了

        # 開始找商品
        product = []
        price = []
        for count in range(1, page + 1):  # 然後把總共的頁數寫成迴圈

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
            if '"price":' in i:
                name = ''.join([x for x in i if x.isdigit()])
                price.append(name)

        for i in useful_inf:
            if '"name":' in i:
                o = i.replace('"', '')
                s = o.find('name:')
                name = o[s + 5:]
                product.append(name)

        new_price = []
        new_product = []
        for i in range(len(price)):
            if price[i] == '':
                pass
            else:
                new_price.append(int(price[i]))
                new_product.append(product[i])

        product_price = dict(zip(new_product, new_price))

        costco_sort_product_price = sorted(
            product_price.items(), key=lambda x: x[1], reverse=False)

        # 家樂福爬蟲

        # , options=options)
        driver = webdriver.Chrome("C:\\Users\\hobbi\\PycharmProjects\\pythonProject1\\chromedriver.exe")
        url = 'https://online.carrefour.com.tw/tw/search?key='
        url += enter_name
        url += '&categoryId='
        driver.get(url)

        total_items_list = driver.find_elements_by_class_name('control')
        total_items_number = float(total_items_list[0].text.strip(
            "筆資料\n最多人購買 價格↓ 上架時間↓").strip('搜尋“').strip(enter_name).strip('” 共"'))

        total_pages = int((total_items_number // 24) + 1)

        product = []
        price = []

        for i in range(total_pages):
            item_list = driver.find_elements_by_class_name(
                'desc-operation-wrapper')
            for item in item_list:
                temp = item.text.split('\n')
                product.append(temp[0])
                price.append(int(temp[-1].strip('$')))

            if total_pages >= 7:
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
            next_button.click()
            time.sleep(1)

        product_price = dict(zip(product, price))
        carefour_sort_product_price = sorted(
            product_price.items(), key=lambda x: x[1], reverse=False)
        # return rtmart_sort_product_price, costco_sort_product_price, carefour_sort_product_price

        global a
        a = rtmart_sort_product_price
        global b
        b = costco_sort_product_price
        global c
        c = carefour_sort_product_price

    def changewords(self):
        self.Block['text'] = a



    """
            print('------')
    def searching(self):

        enter_name = self.buscar.get("1.0", tk.END)

        rtmart_url = 'https://www.rt-mart.com.tw/direct/index.php?action=prod_search&prod_keyword='  # 抓網址
        rtmart_url += enter_name
        rtmart_url += '&auto_date_start=&auto_date_end=&price_range=&price_range_top=&price_range_bottom=&prod_sort_uid=&p_data_num=30&usort=&page='
        rtmart_content = requests.get(rtmart_url)
        soup = BeautifulSoup(rtmart_content.text, 'html.parser')  # 爬網頁內容

        # 這一段是在找頁數
        attr = {'class': 't02'}
        items_number = int(str(soup.find_all('span', attrs=attr)).replace(
            '<span class="t02">', '').replace('</span>', '').replace('[', '').replace(']', ''))  # 找到商品總共有幾項
        page = math.ceil(items_number / 30)  # 大潤發是一頁放30項，所以我就用商品數除一頁放幾項然後無條件進位，就是頁數了

        # 開始找商品
        product = []
        price = []
        for count in range(1, page + 1):  # 然後把總共的頁數寫成迴圈

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
            if '"price":' in i:
                name = ''.join([x for x in i if x.isdigit()])
                price.append(name)

        for i in useful_inf:
            if '"name":' in i:
                o = i.replace('"', '')
                s = o.find('name:')
                name = o[s + 5:]
                product.append(name)

        new_price = []
        new_product = []
        for i in range(len(price)):
            if price[i] == '':
                pass
            else:
                new_price.append(int(price[i]))
                new_product.append(product[i])

        product_price = dict(zip(new_product, new_price))

        costco_sort_product_price = sorted(
            product_price.items(), key=lambda x: x[1], reverse=False)

        # 家樂福爬蟲

        # , options=options)
        driver = webdriver.Chrome("C:\\Users\\hobbi\\PycharmProjects\\pythonProject1\\chromedriver.exe")
        url = 'https://online.carrefour.com.tw/tw/search?key='
        url += enter_name
        url += '&categoryId='
        driver.get(url)

        total_items_list = driver.find_elements_by_class_name('control')
        total_items_number = float(total_items_list[0].text.strip(
            "筆資料\n最多人購買 價格↓ 上架時間↓").strip('搜尋“').strip(enter_name).strip('” 共"'))

        total_pages = int((total_items_number // 24) + 1)

        product = []
        price = []

        for i in range(total_pages):
            item_list = driver.find_elements_by_class_name(
                'desc-operation-wrapper')
            for item in item_list:
                temp = item.text.split('\n')
                product.append(temp[0])
                price.append(int(temp[-1].strip('$')))

            if total_pages >= 7:
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
            next_button.click()
            time.sleep(1)

        product_price = dict(zip(product, price))
        carefour_sort_product_price = sorted(
            product_price.items(), key=lambda x: x[1], reverse=False)

        global a
        a = rtmart_sort_product_price

        global b
        b = costco_sort_product_price

        global c
        c = carefour_sort_product_price

    def changewords(self):

            print('大潤發的最低價格的推薦是：')
            if len(rtmart_sort_product_price) == 0:
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
            if len(costco_sort_product_price) == 0:
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
            if len(carefour_sort_product_price) == 0:
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
"""
"""global a
        a = rtmart_sort_product_price

        global b
        b = costco_sort_product_price

        global c
        c = carefour_sort_product_price"""

information().mainloop()

