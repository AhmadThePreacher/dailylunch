import requests
import json
import re
import io
from datetime import datetime
from lxml import html as lxml_html
import unicodedata
import pdfplumber

def extract_today_menu(full_menu_text, current_day, current_day_upper=None):
    day_str_found = None
    # Normalize the text to handle different Unicode representations (e.g., for 'Å')
    full_menu_text = unicodedata.normalize('NFC', full_menu_text)

    start_index = full_menu_text.find(current_day)
    if start_index != -1:
        day_str_found = current_day
    elif current_day_upper:
        start_index = full_menu_text.find(current_day_upper)
        if start_index != -1:
            day_str_found = current_day_upper

    if start_index == -1:
        return None

    # Find the end of the line containing the day string
    end_of_day_line_index = full_menu_text.find('\n', start_index)
    if end_of_day_line_index == -1:
        # If no newline, the menu is likely on the same line, just after the day string
        menu_start_index = start_index + len(day_str_found)
    else:
        # The menu content starts on the next line
        menu_start_index = end_of_day_line_index + 1

    # Find the start of the next day to determine the end of today's menu
    next_day_start_index = len(full_menu_text)
    search_from_pos = menu_start_index
    for day, day_upper in zip(days_in_swedish.values(), days_in_swedish_upper.values()):
        # Find the earliest occurrence of another day's name to mark the end of the current menu
        for day_variant in [d for d in [day, day_upper] if d]:
            next_day_pos = full_menu_text.find(day_variant, search_from_pos)
            if next_day_pos != -1:
                next_day_start_index = min(next_day_start_index, next_day_pos)

    today_menu = full_menu_text[menu_start_index:next_day_start_index]
    return today_menu.strip()

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
    "Monday": "MÅNDAG",
    "Tuesday": "TISDAG",
    "Wednesday": "ONSDAG",
    "Thursday": "TORSDAG",
    "Friday": "FREDAG", # This was likely fine, but good to be consistent
    "Saturday": "LÖRDAG",
    "Sunday": "SÖNDAG"
}

current_day = days_in_swedish[datetime.now().strftime("%A")]
current_day_upper = days_in_swedish_upper[datetime.now().strftime("%A")]

with open("restaurants.json", "r", encoding="utf-8") as file:
    restaurants = json.load(file)

scraped_menus = {}
for restaurant in restaurants:
    # Handle PDF with dynamic weekly URL
    if restaurant.get("type") == "pdf_weekly":
        try:
            now = datetime.now()
            week_number = f"{now.isocalendar()[1]:02d}" # Pad with leading zero if needed
            year = now.year
            url_params = {'week': week_number, 'year': year}
            pdf_url = restaurant["url_pattern"].format(**url_params)
            
            response = requests.get(pdf_url, timeout=10)
            response.raise_for_status()

            with pdfplumber.open(io.BytesIO(response.content)) as pdf:
                full_menu_text = "\n".join(page.extract_text() for page in pdf.pages)
            
            today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)
            if today_menu:
                if "suffix" in restaurant:
                    today_menu += restaurant["suffix"]
                scraped_menus[restaurant["name"]] = today_menu
            else:
                scraped_menus[restaurant["name"]] = f"No menu available for {current_day}."
        except requests.exceptions.RequestException as e:
            scraped_menus[restaurant["name"]] = f"Could not fetch PDF: {e}"
        continue # Move to the next restaurant

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
            elif restaurant["name"] == "Cicchetti (5 min)":
                today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)
                if today_menu and "OBS=>" in today_menu:
                    today_menu = today_menu.split("OBS=>")[0].strip()
            else:
                today_menu = extract_today_menu(full_menu_text, current_day, current_day_upper)
            
            if today_menu:
                if "suffix" in restaurant:
                    today_menu += restaurant["suffix"]
                scraped_menus[restaurant["name"]] = today_menu
            else:
                scraped_menus[restaurant["name"]] = f"No menu available for {current_day}."
        else:
            scraped_menus[restaurant["name"]] = "Menu container not found on page."
    except requests.exceptions.RequestException as e:
        scraped_menus[restaurant["name"]] = f"Could not fetch page: {e}"


with open("scraped_menus.json", "w", encoding="utf-8") as file:
    json.dump(scraped_menus, file, indent=2, ensure_ascii=False)
