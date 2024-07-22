# import requests
# from bs4 import BeautifulSoup

# # URL of the page to scrape
# url = 'https://www.restaurangspill.se/'

# # Send an HTTP request to fetch the page content
# response = requests.get(url)
# response.raise_for_status()  # Ensure we notice bad responses

# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# # Locate the specific div using its class and id
# div = soup.find('div', class_='flex flex-col gap-4 md:gap-8')

# if div:
#     print(div.get_text(separator='\n', strip=True))
# else:
#     print("Div not found")


import requests
from bs4 import BeautifulSoup
import json

# Load the list of restaurants from the JSON file
with open('restaurants.json', 'r') as file:
    restaurants = json.load(file)

# Dictionary to store the scraped data
scraped_menus = {}

# Loop over each restaurant
for restaurant in restaurants:
    response = requests.get(restaurant['url'])
    response.encoding = 'utf-8'  # Manually set encoding to UTF-8
    html_content = response.text
    soup = BeautifulSoup(response.content, 'html.parser')

    # Dynamically execute the parser string from the JSON file
    div = eval(restaurant['parser'])

    if div:
        print(div.get_text(separator='\n', strip=True))
        scraped_menus[restaurant['name']] = div.get_text(separator='\n', strip=True)

# Write the scraped menus to a new JSON file
with open('scraped_menus.json', 'w', encoding='utf-8') as file:
    json.dump(scraped_menus, file, indent=4, ensure_ascii=False)

print("Scraping completed and data stored in 'scraped_menus.json'")