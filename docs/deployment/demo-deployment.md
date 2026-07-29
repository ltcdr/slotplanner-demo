# Slotplanner Demo – Azure App Service Deployment Guide

This document describes how the Slotplanner **demo** (activities + booking flow) can be deployed to Azure App Service.  
It focuses on the lightweight demo architecture and does not represent the full production deployment of Slotplanner.

The demo consists of:

- A FastAPI backend (activities + bookings)
- A static HTML/CSS/JS frontend
- A small SQLite database
- Basic session-based authentication

The goal of this guide is to outline a simple, reproducible deployment path suitable for showcasing the demo in a cloud environment.

---

## Architecture Overview (Demo)

The demo uses a minimal architecture:

- **Backend:** FastAPI  
- **Frontend:** Static HTML/CSS/JS  
- **Database:** SQLite (file-based, demo only)  
- **Hosting:** Azure App Service  
- **Reverse Proxy / Static Serving:** App Service built‑in static file support or FastAPI `StaticFiles`  
- **CI/CD:** GitHub Actions (optional)

This deployment guide is intentionally lightweight and separate from the full Slotplanner architecture described in the main README.

---

## Folder Structure

The demo is organized as follows:

```
demo/
├── backend/
│   ├── auth.py
│   ├── db.py
│   ├── demo.db
│   ├── main.py
│   ├── models.py
│   ├── router_activities.py
│   ├── router_bookings.py
│   └── services.py
│
└── frontend/
    ├── index.html
    ├── calendar.html
    ├── bookings.html
    ├── styles.css
    ├── demo_calendar.js
    ├── bookings.js
    └── img/
        └── scrnsht.png

```


Azure App Service will host both the backend and the frontend from this structure.

---

## Azure App Service Configuration

### Runtime
- **Python 3.11**
- Linux App Service plan (Free, Basic, or higher)

### Startup Command

Azure App Service requires a startup command to run FastAPI via Gunicorn:

```
gunicorn -k uvicorn.workers.UvicornWorker backend.main:app
```


This command launches the FastAPI application using Uvicorn workers.

### Environment Variables

Add the following App Settings in Azure:

| Key | Value |
|-----|--------|
| `DEMO_DB_PATH` | `/home/site/wwwroot/demo/backend/demo.db` |
| `DEMO_PASSWORD` | Your chosen demo password |

These values are used by the demo backend to locate the SQLite database and protect the demo pages.

---

## SQLite Handling on Azure

SQLite is fully supported for demos on Azure App Service.

Important notes:

- The App Service filesystem is persistent across restarts.
- The SQLite file must be located inside `/home/site/wwwroot/`.
- No migrations or external database services are required.
- This setup is **not** intended for production use.

---

## Serving Static Files

You have two options for serving the demo frontend:


### Option A — Serve via FastAPI

Add this to `main.py`:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="demo/frontend", html=True), name="frontend")
```

This makes the frontend available at the root URL.


### Option B — Use App Service Static File Support

Place all frontend files directly in:

```
/home/site/wwwroot/
```

App Service will automatically serve them.

Both approaches work; Option A keeps backend and frontend together.


## Deployment Steps

1. Create Azure App Service
    - Choose Python 3.11 runtime
    - Select Linux hosting
    - Create a new resource group (optional)

2. Configure App Settings
    - Add:
    - DEMO_DB_PATH
    - DEMO_PASSWORD

3. Upload Demo Files
    - You can deploy using:
        - GitHub Actions
        - ZIP deployment
        - Azure CLI
        - VS Code Azure extension

4. Verify File Structure
    - Ensure the deployed structure matches:

        ```
        /home/site/wwwroot/demo/backend/
        ```

    - and contains:

        - main.py
        - demo.db
        - routers, services, models

5. Add Startup Command
    - In App Service → Configuration → Startup  Command:

        ```
        gunicorn -k uvicorn.workers.UvicornWorker backend.main:app
        ```

6. Restart App Service
    - After configuration changes, restart the service.

7. Access the Demo
    - Your demo will be available at:

    
            https://<your-app-name>.azurewebsites.net


## Security Notes
The demo uses a simple password mechanism.

No sensitive data is stored.

SQLite is used only for demonstration.

The demo is intentionally isolated from the full Slotplanner system.