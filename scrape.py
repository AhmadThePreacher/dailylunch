from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Assuming you have the Chrome WebDriver installed and its path is set in the system PATH
service = Service()

# Initialize the driver with the specified options
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.restaurangspill.se/')

# Find the element using XPath
spill = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div')

print(spill.text)

driver.quit()
