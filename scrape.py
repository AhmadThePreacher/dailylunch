from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get('https://www.restaurangspill.se/')

    # Debug: print page source to check if the content is loading
    print(driver.page_source)

    # Wait up to 15 seconds for the element to be available
    spill = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div'))
    )

    print('Restaurang Spill:')
    print(spill.text)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
