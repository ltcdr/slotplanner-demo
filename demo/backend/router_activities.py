from fastapi import APIRouter, HTTPException
from .services import (
    get_activities, 
    generate_next_week_activities, 
    cleanup_old_activities
)
from .models import Activity

router = APIRouter()

@router.get("/activities", response_model=list[Activity])
def list_activities():
    """
    Returns all demo activities.
    Auto-generates weekly activities if none exist.
    """
    return get_activities()


@router.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: int):
    """
    Returns a single activity by ID.
    """
    activities = get_activities()
    for activity in activities:
        if activity.id == activity_id:
            return activity

    raise HTTPException(status_code=404, detail="Activity not found")


@router.post("/admin/generate_next_week")
def admin_generate_next_week():
    generate_next_week_activities()
    return {"status": "ok", "message": "Next week activities generated"}


@router.post("/admin/cleanup_old")
def admin_cleanup_old():
    cleanup_old_activities()
    return {"status": "ok", "message": "Old activities cleaned up"}