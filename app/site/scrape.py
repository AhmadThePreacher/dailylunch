import requests
import json
import re
from datetime import datetime
from lxml import html as lxml_html

def extract_today_menu(full_menu_text, current_day, current_day_upper=None):
    start_index = full_menu_text.find(current_day)
    if start_index == -1 and current_day_upper:
        start_index = full_menu_text.find(current_day_upper)
    if start_index == -1:
        return None
    next_day_start_index = len(full_menu_text)
    for day, day_upper in zip(days_in_swedish.values(), days_in_swedish_upper.values()):
        if day != current_day and day_upper != current_day_upper:
            next_day_index = full_menu_text.find(day, start_index + len(current_day))
            next_day_upper_index = full_menu_text.find(day_upper, start_index + len(current_day_upper or ""))
            if next_day_index != -1 and next_day_index < next_day_start_index:
                next_day_start_index = next_day_index
            if next_day_upper_index != -1 and next_day_upper_index < next_day_start_index:
                next_day_start_index = next_day_upper_index
    today_menu = full_menu_text[start_index:next_day_start_index].strip()
    return today_menu

days_in_swedish = {
    "Monday": "Måndag",
    "Tuesday": "Tisdag",
    "Wednesday": "Onsdag",
    "Thursday": "Torsdag",
    "Friday": "Fredag",
    "Saturday": "Lördag",
    "Sunday": "Söndag"
}

days_in_swedish_upper = {
    "Monday": "MÅNDAG",
    "Tuesday": "TISDAG",
    "Wednesday": "ONSDAG",
    "Thursday": "TORSDAG",
    "Friday": "FREDAG",
    "Saturday": "LÖRDAG",
    "Sunday": "SÖNDAG"
}

current_day = days_in_swedish[datetime.now().strftime("%A")]
current_day_upper = days_in_swedish_upper[datetime.now().strftime("%A")]

with open("restaurants.json", "r", encoding="utf-8") as file:
    restaurants = json.load(file)

scraped_menus = {}
for restaurant in restaurants:
    try:
        response = requests.get(restaurant["url"], timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        response.encoding = "utf-8"
        tree = lxml_html.fromstring(response.content)
        
        elements = tree.xpath(restaurant["xpath"])
        if elements:
            full_menu_text = "\n".join([elem.text_content().strip() for elem in elements if elem.text_content().strip()])
    
            if restaurant["name"] == "Restaurang Spill (1 min)":
                try:
                    menu_block = full_menu_text.split(current_day.lower())[1]
                    menu_block = menu_block.split("kr")[0] + "kr"
                    today_menu = re.sub(r'^,\s*\d{1,2}/\d{1,2},\s*\d{4}', '', menu_block, 1).strip()
                except IndexError:
                    today_menu = None
            else:
                today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)
                if today_menu and restaurant["name"] == "Cicchetti (5 min)":
                    today_menu += "\n149 kr, bryggkaffe & sallads buffé ingår."
            
            if today_menu:
                scraped_menus[restaurant["name"]] = today_menu
            else:
                scraped_menus[restaurant["name"]] = f"No menu available for {current_day}."
        else:
            scraped_menus[restaurant["name"]] = "Menu container not found on page."
    except requests.exceptions.RequestException as e:
        scraped_menus[restaurant["name"]] = f"Could not fetch page: {e}"


with open("scraped_menus.json", "w", encoding="utf-8") as file:
    json.dump(scraped_menus, file, indent=2, ensure_ascii=False)
