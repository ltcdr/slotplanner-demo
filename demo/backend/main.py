from fastapi import FastAPI
from demo.backend.auth import basic_auth
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .router_activities import router as activities_router
from .router_bookings import router as bookings_router

# Initialize SQLite database
init_db()

app = FastAPI(
    title="Slotplanner Demo Backend",
    description="Minimal demo backend with activities + bookings",
    version="1.0.0",
)
app.middleware("http")(basic_auth)

# ---------------------------------------------------------
# Serve demo frontend (HTML, CSS, JS, images)
# ---------------------------------------------------------
app.mount(
    "/demo/frontend",
    StaticFiles(directory="demo/frontend"),
    name="demo-frontend"
)

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
