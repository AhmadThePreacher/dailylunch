import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json

# Load restaurants from JSON file
def load_restaurants(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to parse the HTML using the provided parser string
def parse_html(soup, parser_str):
    return eval(parser_str)

def scrape_menus():
    restaurants = load_restaurants('restaurants.json')
    conn = sqlite3.connect('menus.db')
    cursor = conn.cursor()

    for restaurant in restaurants:
        url = restaurant['url']
        parser_str = restaurant['parser']
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            menu = parse_html(soup, parser_str)
            
            cursor.execute('INSERT INTO menus (date, restaurant, menu) VALUES (?, ?, ?)', 
                           (datetime.now().date(), restaurant['name'], menu))
            print(f"Scraped menu from {restaurant['name']}: {menu}")
        except Exception as e:
            print(f"Failed to scrape {restaurant['name']}: {e}")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    scrape_menus()
