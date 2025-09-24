import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

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
    response = requests.get(restaurant["url"])
    response.encoding = "utf-8"
    html_content = response.text
    soup = BeautifulSoup(response.content, "html.parser")
    div = eval(restaurant["parser"])
    if div:
        full_menu_text = div.get_text(separator="\n", strip=True)

        if restaurant["name"] == "Ubåtshallen (6min)":
            if "På fredagar" in full_menu_text:
                full_menu_text = full_menu_text.split("På fredagar")[0].strip()

        if restaurant["name"] == "Restaurang Spill (1 min)":
            today_menu = full_menu_text.split("125")[0].strip()
        else:
            today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)
        if today_menu:
            scraped_menus[restaurant["name"]] = today_menu
        else:
            scraped_menus[restaurant["name"]] = f"No menu available for {current_day}."
    else:
        scraped_menus[restaurant["name"]] = "No data available."


with open("scraped_menus.json", "w", encoding="utf-8") as file:
    json.dump(scraped_menus, file, indent=2, ensure_ascii=False)
