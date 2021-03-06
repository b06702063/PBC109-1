import tkinter as tk
from PIL import ImageTk
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

"""第一頁"""


def assign(num):
    x = num


class generator(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.imagetit = ImageTk.PhotoImage(file="tit.png")
        self.mode = tk.Label(self, image=self.imagetit)
        self.imageP = ImageTk.PhotoImage(file="P.png")
        self.price_oriented = tk.Button(self, image=self.imageP)
        self.imageS = ImageTk.PhotoImage(file="S.png")
        self.store_oriented = tk.Button(self, image=self.imageS)
        self.imageM = ImageTk.PhotoImage(file="M.png")
        self.mixed_version = tk.Button(self, image=self.imageM)
        self.price_oriented.grid(row=1, column=0)
        self.store_oriented.grid(row=1, column=1)
        self.mixed_version.grid(row=1, column=2)
        self.mode.grid(row=0, column=1)


gen = generator()
gen.master.title("The cost generator")
gen.mainloop()


class information(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.input_information()

    def input_information(self):
        self.instruction = tk.Label(self, text="Your ingredients")
        self.Block = tk.Text(self, height=40, width=40)
        self.instruction.grid(row=0, column=0)
        self.Block.grid(row=1, column=0)
