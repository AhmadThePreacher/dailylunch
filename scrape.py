from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

Options().add_argument('--headless')
Options().add_argument('--no-sandbox')
Options().add_argument('--disable-dev-shm-usage')

# Assuming you have the Chrome WebDriver installed
driver = webdriver.Chrome()

driver.get('https://www.restaurangspill.se/')

# Find the element using XPath
spill = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div')
driver.quit()

print(spill.text)
