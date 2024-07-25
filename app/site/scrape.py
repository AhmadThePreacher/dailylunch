import requests
from bs4 import BeautifulSoup
import json

# Load the list of restaurants from the JSON file
with open("restaurants.json", "r") as file:
    restaurants = json.load(file)

# Dictionary to store the scraped data
scraped_menus = {}

# Loop over each restaurant
for restaurant in restaurants:
    response = requests.get(restaurant["url"])
    response.encoding = "utf-8"  # Manually set encoding to UTF-8
    html_content = response.text
    soup = BeautifulSoup(response.content, "html.parser")

    # Dynamically execute the parser string from the JSON file
    div = eval(restaurant["parser"])

    if div:
        print(div.get_text(separator="\n", strip=True))
        scraped_menus[restaurant["name"]] = div.get_text(separator="\n", strip=True)

# Write the scraped menus to a new JSON file
with open("scraped_menus.json", "w", encoding="utf-8") as file:
    json.dump(scraped_menus, file, indent=4, ensure_ascii=False)

print("Scraping completed and data stored in 'scraped_menus.json'")
