import { get } from "axios";
import { load } from "cheerio";
import { readFileSync, writeFileSync } from "fs";

// Load the list of restaurants from the JSON file
const restaurants = JSON.parse(readFileSync("restaurants.json"));

// Object to store the scraped data
const scrapedMenus = {};

// Check if the script has already run today
const lastRunDate = new Date(localStorage.getItem("lastRunDate"));
const currentDate = new Date();
const isSameDay =
    lastRunDate.getDate() === currentDate.getDate() &&
    lastRunDate.getMonth() === currentDate.getMonth() &&
    lastRunDate.getFullYear() === currentDate.getFullYear();

if (!isSameDay) {
    // Loop over each restaurant
    restaurants.forEach(async (restaurant) => {
        try {
            const response = await get(restaurant.url, {
                responseEncoding: "utf-8",
            });
            const htmlContent = response.data;
            const $ = load(htmlContent);

            // Dynamically execute the parser string from the JSON file
            // Note: Using eval() in this context is generally discouraged due to security risks
            const div = eval(restaurant.parser);

            if (div) {
                const menuText = div.text().replace(/\s\s+/g, "\n").trim();
                console.log(menuText);
                scrapedMenus[restaurant.name] = menuText;
            }
        } catch (error) {
            console.error(
                `Error scraping ${restaurant.name}: ${error.message}`
            );
        }
    });

    // Write the scraped menus to a new JSON file
    writeFileSync("scraped_menus.json", JSON.stringify(scrapedMenus, null, 4));

    // Update the last run date in local storage
    localStorage.setItem("lastRunDate", currentDate);
}

console.log("Scraping completed and data stored in 'scraped_menus.json'");
