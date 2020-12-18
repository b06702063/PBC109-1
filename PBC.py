import requests
from bs4 import BeautifulSoup
response = requests.get(
    "https://www.costco.com.tw/Food/Chilled-Fresh-Foods/c/909")  # 好市多網站
soup = BeautifulSoup(response.text, "html.parser")  # html parser

attr = {"class": "product-price-amount"}
products = soup.find_all("span", atts=attr)

for product in products:
    print(product)
    print("________")

 """ 介面第一張"""
from PIL import ImageTk
import tkinter as tk

"""第一頁"""

class generator(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.mode = tk.Label(self, text="MODE")
        self.imageP = ImageTk.PhotoImage(file="P.png")
        self.price_oriented = tk.Button(self, image=self.imageP,  command=self.strconvert)
        self.store_oriented = tk.Button(self, text = "同一家店", )
        self.mixed_version = tk.Button(self, text = "中庸", )
        self.price_oriented.grid(row=1, column = 0)
        self.store_oriented.grid(row=1, column = 1)
        self.mixed_version.grid(row=1, column = 2)
        self.mode.grid(row=0, column = 1)

    def strconvert(self):
        self.price_oriented.configure(text = "最高價")

gen =generator()
gen.master.title("The cost generator")
gen.mainloop()
