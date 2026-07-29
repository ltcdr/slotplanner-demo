// =========================================================
// Demo Calendar JS
// Fetches activities, renders calendar, handles booking
// =========================================================

let currentWeekStart = getStartOfWeek(new Date());
let activities = [];

// ---------------------------------------------------------
// Helpers
// ---------------------------------------------------------

function getStartOfWeek(date) {
    const d = new Date(date);
    const day = d.getDay(); // 0 = Sunday
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Monday as first day
    return new Date(d.setDate(diff));
}

function addDays(date, days) {
    const d = new Date(date);
    d.setDate(d.getDate() + days);
    return d;
}

function formatTime(dt) {
    return dt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function formatDate(dt) {
    return dt.toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" });
}

// ---------------------------------------------------------
// Fetch activities from backend
// ---------------------------------------------------------

async function loadActivities() {
    const res = await fetch("/demo/activities");
    activities = await res.json();
    renderCalendar();
}

// ---------------------------------------------------------
// Calendar Rendering
// ---------------------------------------------------------

function renderCalendar() {
    const container = document.getElementById("demo-calendar-container");
    container.innerHTML = "";

    const grid = document.createElement("div");
    grid.className = "cal-grid";

    // -----------------------------------------------------
    // Gutter (hours)
    // -----------------------------------------------------
    const gutter = document.createElement("div");
    gutter.className = "cal-gutter";

    const gutterHeader = document.createElement("div");
    gutterHeader.className = "cal-gutter-header";
    gutter.appendChild(gutterHeader);

    for (let h = 8; h < 20; h++) {
        const hourLabel = document.createElement("div");
        hourLabel.className = "cal-hour-label";
        hourLabel.textContent = `${h}:00`;
        gutter.appendChild(hourLabel);
    }

    grid.appendChild(gutter);

    // -----------------------------------------------------
    // 7 day columns
    // -----------------------------------------------------
    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
        const dayDate = addDays(currentWeekStart, dayIndex);

        const dayCol = document.createElement("div");
        dayCol.className = "cal-day-col";

        // Header
        const header = document.createElement("div");
        header.className = "cal-day-header";
        header.textContent = formatDate(dayDate);
        dayCol.appendChild(header);

        // Body
        const body = document.createElement("div");
        body.className = "cal-day-body";

        // Hour cells
        for (let h = 8; h < 20; h++) {
            const hourCell = document.createElement("div");
            hourCell.className = "cal-hour-cell";
            body.appendChild(hourCell);
        }

        // -------------------------------------------------
        // Activities for this day
        // -------------------------------------------------
        const todaysActivities = activities.filter(a => {
            const start = new Date(a.start_time);
            return start.toDateString() === dayDate.toDateString();
        });

        todaysActivities.forEach(a => {
            const start = new Date(a.start_time);
            const end = new Date(a.end_time);

            const startHour = start.getHours() + start.getMinutes() / 60;
            const endHour = end.getHours() + end.getMinutes() / 60;

            // Skip activities outside visible range
            if (startHour < 8 || startHour >= 20) return;

            const top = (startHour - 8) * 60;
            const height = (endHour - startHour) * 60;

            // Activity card
            const card = document.createElement("div");
            card.className = "cal-activity";
            card.style.top = `${top}px`;
            card.style.height = `${height}px`;

            // Title
            const titleWrapper = document.createElement("div");
            const titleStrong = document.createElement("strong");
            titleStrong.textContent = a.title;
            titleWrapper.appendChild(titleStrong);

            // Time
            const timeEl = document.createElement("div");
            timeEl.className = "cal-activity-time";
            timeEl.textContent = `${formatTime(start)} - ${formatTime(end)}`;

            card.appendChild(titleWrapper);
            card.appendChild(timeEl);

            card.onclick = () => openModal(a);

            body.appendChild(card);
        });

        dayCol.appendChild(body);
        grid.appendChild(dayCol);
    }

    container.appendChild(grid);
}

// ---------------------------------------------------------
// Modal
// ---------------------------------------------------------

let selectedActivity = null;

function openModal(activity) {
    selectedActivity = activity;

    const titleEl = document.getElementById("modal-title");
    const timeEl = document.getElementById("modal-time");

    const start = new Date(activity.start_time);
    const end = new Date(activity.end_time);

    titleEl.textContent = activity.title;
    timeEl.textContent = `${formatTime(start)} - ${formatTime(end)}`;

    document.getElementById("activity-modal").classList.remove("hidden");
}

function closeModal() {
    document.getElementById("activity-modal").classList.add("hidden");
    selectedActivity = null;
}

// ---------------------------------------------------------
// Booking
// ---------------------------------------------------------

async function requestBooking() {
    if (!selectedActivity) return;

    const res = await fetch(`/demo/book?activity_id=${selectedActivity.id}`, {
        method: "POST"
    });

    if (res.ok) {
        alert("Booking created!");
        closeModal();
    } else {
        alert("Booking failed.");
    }
}

// ---------------------------------------------------------
// Week navigation
// ---------------------------------------------------------

function changeWeek(offset) {
    if (offset === 0) {
        currentWeekStart = getStartOfWeek(new Date());
    } else {
        currentWeekStart = addDays(currentWeekStart, offset * 7);
    }

    loadActivities();
}

// ---------------------------------------------------------
// Init
// ---------------------------------------------------------

window.onload = () => {
    loadActivities();

    document.getElementById("modal-book-btn")
        .addEventListener("click", requestBooking);
};
