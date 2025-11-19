function fetchMenus() {
    return fetch("scraped_menus.json").then((response) => {
        if (!response.ok) throw new Error("Could not fetch menus.");
        return response.json();
    });
}

function fetchDateTime() {
    return fetch("dateTime.json").then((response) => {
        if (!response.ok) throw new Error("Could not fetch update time.");
        return response.json();
    });
}

function fetchRestaurants() {
    return fetch("restaurants.json").then((response) => {
        if (!response.ok) throw new Error("Could not fetch restaurants.");
        return response.json();
    });
}

Promise.all([fetchMenus(), fetchDateTime(), fetchRestaurants()])
    .then(([menus, dateTime, restaurants]) => {
        // Create a map of restaurant names to their link info
        const restaurantLinks = {};
        restaurants.forEach((restaurant) => {
            if (restaurant.takeaway_link && restaurant.takeaway_text) {
                restaurantLinks[restaurant.name] = {
                    url: restaurant.takeaway_link,
                    text: restaurant.takeaway_text,
                };
            }
        });
        const dateTimeContainer = document.getElementById("dateTime");
        dateTimeContainer.textContent = `Last Updated: ${dateTime.last_run_day}, ${dateTime.last_run_date} at ${dateTime.last_run_time}`;

        const menuContainer = document.getElementById("menu-container");
        for (const [restaurant, menu] of Object.entries(menus)) {
            const restaurantDiv = document.createElement("div");
            restaurantDiv.classList.add("restaurant");

            const name = document.createElement("h2");
            name.textContent = restaurant;
            restaurantDiv.appendChild(name);

            const menuText = document.createElement("p");
            menuText.innerHTML = menu.replace(/\n/g, "<br>");
            restaurantDiv.appendChild(menuText);

            if (restaurantLinks[restaurant]) {
                const linkElement = document.createElement("a");
                linkElement.href = restaurantLinks[restaurant].url;
                linkElement.textContent = restaurantLinks[restaurant].text;
                linkElement.target = "_blank";
                linkElement.classList.add("takeaway-link");
                restaurantDiv.appendChild(linkElement);
            }

            menuContainer.appendChild(restaurantDiv);
        }
    })
    .catch((error) => {
        console.error("Error loading page data:", error);
        document.getElementById(
            "menu-container"
        ).innerHTML = `<p style="color: red;">${error.message}</p>`;
    });
