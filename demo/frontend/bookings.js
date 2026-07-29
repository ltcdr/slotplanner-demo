let activitiesMap = {};

async function loadActivities() {
    const res = await fetch("/demo/activities");
    const activities = await res.json();

    activitiesMap = {};
    activities.forEach(a => {
        activitiesMap[a.id] = a;   // store full activity object
    });
}

async function loadBookings() {
    const response = await fetch("/demo/bookings");

    if (!response.ok) {
        alert("Failed to load bookings");
        return;
    }

    const bookings = await response.json();
    const container = document.getElementById("bookings-container");
    const noBookings = document.getElementById("no-bookings");

    container.innerHTML = "";

    if (bookings.length === 0) {
        noBookings.style.display = "block";
        return;
    }

    noBookings.style.display = "none";

    bookings.forEach(b => {
        const card = document.createElement("div");
        card.className = "feature";

        // Title: Booking #ID
        const title = document.createElement("h4");
        title.textContent = `Booking #${b.id}`;
        card.appendChild(title);

        // Activity ID
        const pActivity = document.createElement("p");
        const strongActivity = document.createElement("strong");
        strongActivity.textContent = "Activity ID:";
        pActivity.appendChild(strongActivity);
        pActivity.append(` ${b.activity_id}`);
        card.appendChild(pActivity);

        // Activity title
        const pTitle = document.createElement("p");
        const strongTitle = document.createElement("strong");
        strongTitle.textContent = "Activity:";
        pTitle.appendChild(strongTitle);

        const activity = activitiesMap[b.activity_id];
        const activityTitle = activity ? activity.title : "(unknown)";
        pTitle.append(` ${activityTitle}`);
        card.appendChild(pTitle);

        // Created timestamp
        const pCreated = document.createElement("p");
        const strongCreated = document.createElement("strong");
        strongCreated.textContent = "Booking created:";
        pCreated.appendChild(strongCreated);

        const createdDate = new Date(b.created_at).toLocaleString();
        pCreated.append(` ${createdDate}`);
        card.appendChild(pCreated);

        container.appendChild(card);
    });
}

async function init() {
    await loadActivities();
    await loadBookings();
}

init();
