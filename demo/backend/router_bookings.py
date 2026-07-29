from fastapi import APIRouter, HTTPException
from .services import create_booking, get_bookings, reset_bookings
from .models import Booking

router = APIRouter()


@router.post("/book", response_model=Booking)
def book_activity(activity_id: int):
    """
    Creates a booking for the given activity_id.
    """
    try:
        booking = create_booking(activity_id)
        return booking
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bookings", response_model=list[Booking])
def list_bookings():
    """
    Returns all bookings.
    """
    return get_bookings()


@router.post("/reset_bookings")
def clear_bookings():
    """
    Deletes all bookings.
    Useful for demo auto-reset.
    """
    reset_bookings()
    return {"status": "ok", "message": "Bookings reset"}
