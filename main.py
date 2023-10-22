import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


URL = "https://www.tradewheel.com/suppliers/"


driver = webdriver.Chrome()
driver.get(URL)


items = driver.find_elements(
    By.CSS_SELECTOR, "div.row div.col-xs-6.col-sm-4.col-md-3.link_box.ind_box a span"
)
all_categories = list(items[30:-1])
"".replace(",", "")

# print(len(all_categories))
# for supplier_cat in all_categories:
#     supplier_cat.click
#     print(supplier_cat.text)


driver.quit()


all_categories[0].click()
company_name = driver.find_elements(
    By.CSS_SELECTOR,
    "body > div:nth-child(5) > div:nth-child(2) > div.col-md-10.col-lg-10.col-sm-12.col-xs-12 > div:nth-child(2) > div:nth-child(1) > h2 > a",
)
for i in company_name:
    print(i.text)
