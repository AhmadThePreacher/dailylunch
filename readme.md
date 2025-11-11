# Daily Lunch Scraper

Tired of checking multiple restaurant websites every day just to see the lunch menu? This project automates the process by scraping the daily lunch menus from a list of restaurants and displaying them on a single, clean webpage.

The scraping process is designed to be run automatically (e.g., via a GitHub Action), ensuring the menus are always up-to-date.

## Features

-   **Multi-Source Scraping**: Fetches menus from various restaurant websites.
-   **Flexible Parsing**: Handles both plain HTML and PDF menus.
-   **Dynamic URL Support**: Supports weekly PDF menus where the URL changes based on the current week and year.
-   **Today-Only Focus**: Intelligently extracts only the menu for the current day from a full week's listing.
-   **Simple Frontend**: Displays all menus on a clean, responsive, and easy-to-read webpage.
-   **Easily Extendable**: Adding new restaurants is as simple as adding an entry to a JSON file.

## How It Works

1.  A Python script (`app/site/scrape.py`) reads a list of restaurants from `app/site/restaurants.json`.
2.  For each restaurant, it fetches the menu from the specified URL. It can handle standard webpages and direct links to PDF files.
3.  Using libraries like `lxml` for HTML and `pdfplumber` for PDFs, it parses the content.
4.  It identifies and extracts only the menu items for the current day, handling various text formats and encodings.
5.  The scraped menus are saved into a single `app/site/scraped_menus.json` file.
6.  The static webpage (`app/site/index.html`) uses vanilla JavaScript to fetch the JSON file and dynamically render the menus for display.

## Technologies Used

-   Python
-   **Backend & Scraping**:
    -   `requests`: For making HTTP requests to fetch web pages and PDFs.
    -   `lxml`: For parsing and querying HTML content with XPath.
    -   `pdfplumber`: For extracting text content from PDF files.
-   **Frontend**:
-   HTML, CSS, and vanilla JavaScript for the frontend.

## Project Structure

```
dailylunch/
├── .github/workflows/   # (Optional) For GitHub Actions automation
├── app/
│   └── site/
│       ├── scrape.py             # The main Python scraper script.
│       ├── restaurants.json      # List of restaurants to scrape.
│       ├── scraped_menus.json    # Output file with scraped data.
│       ├── index.html            # The main HTML file for the webpage.
│       ├── style.css             # Styles for the webpage.
│       ├── script.js             # JavaScript to fetch and display menus.
│       └── dateTime.json         # Logs the last run time of the scraper.
├── requirements.txt     # Python dependencies.
└── readme.md            # This file.
```

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

## Local Usage

To run the scraper manually and update the menus:

1.  Navigate to the site directory:
    ```bash
    cd app/site/
    ```
2.  Run the scraper script:
    ```bash
    python scrape.py
    ```
    This will update `scraped_menus.json` and `dateTime.json`. You can then open `index.html` in your browser to see the results.

## Contributing

Contributions are welcome! The easiest way to contribute is by adding a new restaurant or improving the scraper's logic.

### Adding a New Restaurant

1.  **Fork the repository.**
2.  **Open `app/site/restaurants.json` and add a new JSON object to the list.**
    -   For a standard HTML page, you will need `name`, `url`, and `xpath`.
        -   `name`: The name of the restaurant (e.g., `"My Favorite Cafe (10 min)"`).
        -   `url`: The direct URL to the restaurant's lunch menu page.
        -   `xpath`: An XPath expression to find the HTML element(s) containing the menu text.
    -   For a weekly PDF, you will need `name`, `type: "pdf_weekly"`, and `url_pattern`.
        -   The `url_pattern` should contain placeholders for `{year}` and `{week}` (e.g., `"https://example.com/menu-w{week}-{year}.pdf"`).
3.  **Test your changes** by running `python app/site/scrape.py` and checking the output in `scraped_menus.json`.
    -   If the standard day-parsing logic in `scrape.py` doesn't work for the new site, you may need to add custom handling logic for that restaurant within the script's main loop.
4.  **Commit your changes and create a Pull Request.**

## License

This project is open-source and available under the MIT License.
