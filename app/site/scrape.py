# import requests
# from bs4 import BeautifulSoup
# import json

# # Load the list of restaurants from the JSON file
# with open("restaurants.json", "r") as file:
#     restaurants = json.load(file)

# # Dictionary to store the scraped data
# scraped_menus = {}

# # Loop over each restaurant
# for restaurant in restaurants:
#     response = requests.get(restaurant["url"])
#     response.encoding = "utf-8"  # Manually set encoding to UTF-8
#     html_content = response.text
#     soup = BeautifulSoup(response.content, "html.parser")

#     # Dynamically execute the parser string from the JSON file
#     div = eval(restaurant["parser"])

#     if div:
#         print(div.get_text(separator="\n", strip=True))
#         scraped_menus[restaurant["name"]] = div.get_text(separator="\n", strip=True)

# # Write the scraped menus to a new JSON file
# with open("scraped_menus.json", "w", encoding="utf-8") as file:
#     json.dump(scraped_menus, file, indent=4, ensure_ascii=False)

# print("Scraping completed and data stored in 'scraped_menus.json'")


import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Map English days to Swedish days, including uppercase for Saltimporten
days_in_swedish = {
    "Monday": "Måndag",
    "Tuesday": "Tisdag",
    "Wednesday": "Onsdag",
    "Thursday": "Torsdag",
    "Friday": "Fredag",
    "Saturday": "Lördag",
    "Sunday": "Söndag"
}

# Map English days to Swedish uppercase days for Saltimporten
days_in_swedish_upper = {
    "Monday": "MÅNDAG",
    "Tuesday": "TISDAG",
    "Wednesday": "ONSDAG",
    "Thursday": "TORSDAG",
    "Friday": "FREDAG",
    "Saturday": "LÖRDAG",
    "Sunday": "SÖNDAG"
}

# Get the current day in Swedish
current_day = days_in_swedish[datetime.now().strftime("%A")]
current_day_upper = days_in_swedish_upper[datetime.now().strftime("%A")]

# Load the list of restaurants from the JSON file
with open("restaurants.json", "r") as file:
    restaurants = json.load(file)

# Dictionary to store the scraped data
scraped_menus = {}

# Function to extract today's menu from the full text
def extract_today_menu(full_menu_text, current_day, current_day_upper=None):
    # Try finding today's menu in the normal case
    start_index = full_menu_text.find(current_day)
    
    # If not found, try finding in the uppercase case (for Saltimporten)
    if start_index == -1 and current_day_upper:
        start_index = full_menu_text.find(current_day_upper)
        
    if start_index == -1:
        return None  # Couldn't find today's menu

    # Find the start of the next day's menu
    next_day_start_index = len(full_menu_text)
    for day, day_upper in zip(days_in_swedish.values(), days_in_swedish_upper.values()):
        if day != current_day and day_upper != current_day_upper:
            next_day_index = full_menu_text.find(day, start_index + len(current_day))
            next_day_upper_index = full_menu_text.find(day_upper, start_index + len(current_day_upper or ""))

            if next_day_index != -1 and next_day_index < next_day_start_index:
                next_day_start_index = next_day_index
            if next_day_upper_index != -1 and next_day_upper_index < next_day_start_index:
                next_day_start_index = next_day_upper_index

    # Extract and return today's menu
    today_menu = full_menu_text[start_index:next_day_start_index].strip()
    return today_menu

# Loop over each restaurant
for restaurant in restaurants:
    response = requests.get(restaurant["url"])
    response.encoding = "utf-8"  # Manually set encoding to UTF-8
    html_content = response.text
    soup = BeautifulSoup(response.content, "html.parser")

    # Dynamically execute the parser string from the JSON file
    div = eval(restaurant["parser"])

    if div:
        # Correctly decode the text if needed
        full_menu_text = div.get_text(separator="\n", strip=True)
        
        # Special handling for Restaurang Spill (no need to filter by day)
        if restaurant["name"] == "Restaurang Spill":
            today_menu = full_menu_text  # Use the full menu text as is
        else:
            # Handle other restaurants with day filtering
            today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)

        if today_menu:
            print(f"Today's menu for {restaurant['name']}:\n{today_menu}\n")
            scraped_menus[restaurant["name"]] = today_menu
        else:
            print(f"No menu found for {restaurant['name']} on {current_day}.")
            scraped_menus[restaurant["name"]] = f"No menu available for {current_day}."
    else:
        print(f"No data could be extracted for {restaurant['name']}.")
        scraped_menus[restaurant["name"]] = "No data available."

# Write the scraped menus to a new JSON file
with open("scraped_menus.json", "w", encoding="utf-8") as file:
    json.dump(scraped_menus, file, indent=2, ensure_ascii=False)

print("Scraping completed and today's data stored in 'scraped_menus.json'")
