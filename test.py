import requests
from bs4 import BeautifulSoup
response = requests.get("https://www.costco.com.tw/Food/c/C8")
soup = BeautifulSoup(response.text, "html.parser")
print(soup)