import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def send_adaptive_card_to_teams(webhook_url, card_payload):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, headers=headers, json=card_payload)
    
    if response.status_code not in [200, 202]:
        raise ValueError(f"Request to Teams returned an error {response.status_code}, the response is:\n{response.text}")

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

def create_adaptive_card_payload(menus):
    today_date = datetime.now().strftime("%Y-%m-%d")
    card_content = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
            {
                "type": "TextBlock",
                "text": f"**TODAY'S MENUS ({today_date})**",
                "horizontalAlignment": "Center",
                "size": "ExtraLarge",
                "style": "heading",
                "weight": "Bolder"
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "View on the Web",
                "url": "https://daily-lunch.onrender.com/"
            }
        ]
    }
    for restaurant, menu in menus.items():
        card_content["body"].append({
            "type": "TextBlock",
            "text": f"{restaurant}:",
            "style": "heading",
            "weight": "Bolder",
            "size": "Large",
            "separator": True,
            "spacing": "ExtraLarge"

        })
        card_content["body"].append({
            "type": "TextBlock",
            "text": menu.replace('\n', '\\\n'),
            "wrap": True
        })
    card_payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": card_content
            }
        ]
    }
    return card_payload

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
        if restaurant["name"] == "Restaurang Spill (6min)":
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

adaptive_card_payload = create_adaptive_card_payload(scraped_menus)

webhook_url = "https://prod-149.westeurope.logic.azure.com:443/workflows/40403b70d0fa49ff928e9ac2f2f5c2cc/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=EkiM3EjfODxur9SEeusqOQEyFHQmhvrp--OKikf2UJQ"
send_adaptive_card_to_teams(webhook_url, adaptive_card_payload)