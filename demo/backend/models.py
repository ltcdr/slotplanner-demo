from datetime import datetime
from pydantic import BaseModel

class Activity(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime

class Booking(BaseModel):
    id: int
    activity_id: int
    created_at: datetime
