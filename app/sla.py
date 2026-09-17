from datetime import date, timedelta
FROZEN_NOW = date(2026, 9, 25)
def business_days_since(opened: str) -> int:
    start = date.fromisoformat(opened); days = 0
    while start < FROZEN_NOW:
        start += timedelta(days=1)
        if start.weekday() < 5: days += 1
    return days
def add_business_days(opened: str, days: int) -> str:
    d = date.fromisoformat(opened)
    while days:
        d += timedelta(days=1)
        if d.weekday() < 5: days -= 1
    return d.isoformat()
