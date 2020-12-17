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
