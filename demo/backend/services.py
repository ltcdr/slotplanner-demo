from datetime import datetime, timedelta
from .db import get_connection
from .models import Activity, Booking


# ---------------------------------------------------------
# ACTIVITIES
# ---------------------------------------------------------

def generate_activities_this_week():
    """
    Clears the activities table and inserts realistic demo activities
    for the current week.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Clear existing activities
    cur.execute("DELETE FROM activities;")

    # Determine Monday of the current week
    today = datetime.now().date()
    weekday = today.weekday()  # Monday = 0
    monday = today - timedelta(days=weekday)

    def dt(day_offset, hour, minute=0):
        """Helper to build datetime for this week's activities."""
        d = monday + timedelta(days=day_offset)
        return datetime(d.year, d.month, d.day, hour, minute)

    activities = [
        # Monday
        ("Breakfast", dt(0, 10), dt(0, 12)),

        # Wednesday
        ("Yoga Class", dt(2, 15), dt(2, 16)),

        # Friday
        ("Walk in the Park", dt(4, 14), dt(4, 15, 30)),
    ]

    for title, start, end in activities:
        cur.execute("""
            INSERT INTO activities (title, start_time, end_time)
            VALUES (?, ?, ?);
        """, (title, start.isoformat(), end.isoformat()))

    conn.commit()
    conn.close()


def get_activities():
    """
    Returns all activities as Pydantic Activity models.
    If the table is empty, auto-generate weekly activities.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM activities;")
    rows = cur.fetchall()

    # Auto-generate if empty
    if not rows:
        generate_activities_this_week()
        cur.execute("SELECT * FROM activities;")
        rows = cur.fetchall()

    conn.close()

    return [
        Activity(
            id=row["id"],
            title=row["title"],
            start_time=datetime.fromisoformat(row["start_time"]),
            end_time=datetime.fromisoformat(row["end_time"])
        )
        for row in rows
    ]


def generate_next_week_activities():
    """
    Inserts realistic demo activities for NEXT week.
    Called by Azure Functions every Friday.
    """
    conn = get_connection()
    cur = conn.cursor()

    today = datetime.now().date()
    weekday = today.weekday()  # Monday = 0

    # Monday of next week
    next_monday = today + timedelta(days=(7 - weekday))

    print("[INFO] Generating next week activities starting:", next_monday)

    # Check if next week already exists
    cur.execute("""
        SELECT COUNT(*) FROM activities
        WHERE date(start_time) >= ? AND date(start_time) < ?;
    """, (
        next_monday.isoformat(),
        (next_monday + timedelta(days=7)).isoformat()
    ))

    count = cur.fetchone()[0]
    if count > 0:
        print("[INFO] Next week activities already exist. Skipping generation.")
        conn.close()
        return

    def dt(day_offset, hour, minute=0):
        """Helper to build datetime for next week's activities."""
        d = next_monday + timedelta(days=day_offset)
        return datetime(d.year, d.month, d.day, hour, minute)

    activities = [
        ("Breakfast", dt(0, 10), dt(0, 12)),       # Monday
        ("Yoga Class", dt(2, 15), dt(2, 16)),      # Wednesday
        ("Walk in the Park", dt(4, 14), dt(4, 15, 30)),  # Friday
    ]

    for title, start, end in activities:
        cur.execute("""
            INSERT INTO activities (title, start_time, end_time)
            VALUES (?, ?, ?);
        """, (title, start.isoformat(), end.isoformat()))

    conn.commit()
    conn.close()


def cleanup_old_activities():
    """
    Deletes activities older than 2 weeks.
    Called by Azure Functions weekly.
    """
    conn = get_connection()
    cur = conn.cursor()

    cutoff = datetime.now() - timedelta(weeks=2)

    print("[INFO] Cleaning up activities older than:", cutoff)

    cur.execute("""
        DELETE FROM activities
        WHERE end_time < ?;
    """, (cutoff.isoformat(),))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# BOOKINGS
# ---------------------------------------------------------

def create_booking(activity_id: int) -> Booking:
    """
    Creates a booking for the given activity_id.
    """
    conn = get_connection()
    cur = conn.cursor()

    created_at = datetime.now().isoformat()

    cur.execute("""
        INSERT INTO bookings (activity_id, created_at)
        VALUES (?, ?);
    """, (activity_id, created_at))

    booking_id = cur.lastrowid

    if booking_id is None:
        raise RuntimeError("Failed to insert booking into database")

    conn.commit()
    conn.close()

    return Booking(
        id=booking_id,
        activity_id=activity_id,
        created_at=datetime.fromisoformat(created_at)
    )


def get_bookings():
    """
    Returns all bookings as Pydantic Booking models.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings;")
    rows = cur.fetchall()
    conn.close()

    return [
        Booking(
            id=row["id"],
            activity_id=row["activity_id"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
        for row in rows
    ]


def reset_bookings():
    """
    Deletes all bookings.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings;")
    conn.commit()
    conn.close()
