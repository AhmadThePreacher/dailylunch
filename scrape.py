# import requests
# from bs4 import BeautifulSoup
# import sqlite3
# from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


# Assuming you have the Chrome WebDriver installed
driver = webdriver.Chrome()

driver.get('https://www.restaurangspill.se/')

# Find the element using XPath
spill = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div')

print(spill.text)

driver.quit()
