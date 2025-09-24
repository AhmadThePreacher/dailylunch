# Daily Lunch Scraper

This project scrapes the daily lunch menus from nearby restaurants and displays them on a single, clean webpage. It also sends a daily notification with the menus to a Microsoft Teams channel.

The process is automated: a Python script fetches the data, generates a static JSON file for the website, and pushes the results to the repository.

## How It Works

1.  A Python script (`app/site/scrape.py`) reads a list of restaurants from `app/site/restaurants.json`.
2.  For each restaurant, it fetches the menu page URL and parses the HTML using `BeautifulSoup` to find the menu content.
3.  It extracts the menu for the current day and handles restaurant-specific formatting.
4.  The scraped menus are saved to `app/site/scraped_menus.json`.
5.  The static webpage (`app/site/index.html`) uses JavaScript to fetch this JSON file and dynamically display the menus.
6.  The script also formats the menus into a Microsoft Teams Adaptive Card and sends it to a pre-configured webhook.

## Technologies Used

-   Python
-   `requests` for making HTTP requests.
-   `BeautifulSoup4` for parsing HTML.
-   HTML, CSS, and vanilla JavaScript for the frontend.

## Installation

1.  **Clone the repository:**

    ```bash
    gh repo clone AhmadThePreacher/dailylunch
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd dailylunch
    ```

3.  **(Recommended) Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the scraper manually and update the menus:

1.  Navigate to the site directory:
    ```bash
    cd app/site
    ```
2.  Run the scraper script:
    `bash
python scrape.py
`
    This will update the `scraped_menus.json` file. You can then open `index.html` in your browser to see the results locally.

## Contributing

Contributions are welcome! The easiest way to contribute is by adding a new restaurant.

1.  **Fork the repository.**
2.  **Add a new restaurant to `app/site/restaurants.json`:**
    -   Open the `app/site/restaurants.json` file.
    -   Add a new JSON object to the list with the following keys:
        -   `name`: The name of the restaurant (e.g., `"My Favorite Cafe (10 min)"`).
        -   `url`: The direct URL to the restaurant's lunch menu page.
        -   `parser`: A string containing a Python expression for `BeautifulSoup` to find the HTML element that contains the full week's menu. For example: `"soup.find('div', class_='menu-container')"`.
3.  **Test your changes** by running `python app/site/scrape.py` and checking the output in `scraped_menus.json`.
    -   If the standard day-parsing logic in `scrape.py` doesn't work for your new restaurant, you may need to add custom handling logic within the main loop of the script.
4.  **Commit your changes and create a Pull Request.**
