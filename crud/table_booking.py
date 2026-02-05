from datetime import datetime, date
from core.db_settings import execute_query


def get_filtered_durations(booking_date_str: str):
    """Return only matching time intervals based on a date."""
    query = "SELECT id, from_time, to_time FROM durations ORDER BY from_time;"
    all_slots = execute_query(query, fetch="all")

    if not all_slots:
        return []

    today = date.today()

    selected_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
    now_time = datetime.now().time()

    filtered_slots = []
    for slot in all_slots:
        if selected_date == today:
            if slot['from_time'] > now_time:
                filtered_slots.append(slot)
        elif selected_date > today:
            filtered_slots.append(slot)

    return filtered_slots


def get_free_tables(duration_id: int, booking_date: str):
    """Return empty tables (1-50) for the selected time and date."""
    query = """
        SELECT table_number FROM orders 
        WHERE duration_id = %s AND create_at::date = %s AND status != 'cancelled';
    """
    rows = execute_query(query, (duration_id, booking_date), fetch="all")

    occupied_tables = []
    if rows:
        occupied_tables = [row['table_number'] for row in rows]

    free_tables = [t for t in range(1, 51) if t not in occupied_tables]

    return free_tables