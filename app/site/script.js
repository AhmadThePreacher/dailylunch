fetch("scraped_menus.json")
    .then((response) => response.json())
    .then((data) => {
        const container = document.getElementById("menu-container");
        for (const [restaurant, menu] of Object.entries(data)) {
            const restaurantDiv = document.createElement("div");
            restaurantDiv.classList.add("restaurant");

            const name = document.createElement("h2");
            name.textContent = restaurant;
            restaurantDiv.appendChild(name);

            const menuText = document.createElement("p");
            menuText.innerHTML = menu.replace(/\n/g, "<br>");
            restaurantDiv.appendChild(menuText);

            container.appendChild(restaurantDiv);
        }
    })
    .catch((error) => console.error("Error loading the menus:", error));
