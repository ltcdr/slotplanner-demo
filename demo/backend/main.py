from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth import basic_auth
from .db import init_db
from .router_activities import router as activities_router
from .router_bookings import router as bookings_router


# Get path string from here to frontend folder
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


# Initialize SQLite database
init_db()

app = FastAPI(
    title="Slotplanner Demo Backend",
    description="Minimal demo backend with activities + bookings",
    version="1.0.0",
)

app.middleware("http")(basic_auth)


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------
app.include_router(activities_router, prefix="/demo")
app.include_router(bookings_router, prefix="/demo")


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/demo/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------
# Serve demo frontend (HTML, CSS, JS, images)
# ---------------------------------------------------------
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="demo-frontend"
)
