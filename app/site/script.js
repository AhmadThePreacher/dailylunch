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

Promise.all([fetchMenus(), fetchDateTime()])
    .then(([menus, dateTime]) => {
        // Display the last updated time
        const dateTimeContainer = document.getElementById("dateTime");
        dateTimeContainer.textContent = `Last Updated: ${dateTime.last_run_day}, ${dateTime.last_run_date} at ${dateTime.last_run_time}`;

        // Display the menus
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

            menuContainer.appendChild(restaurantDiv);
        }
    })
    .catch((error) => {
        console.error("Error loading page data:", error);
        document.getElementById(
            "menu-container"
        ).innerHTML = `<p style="color: red;">${error.message}</p>`;
    });
