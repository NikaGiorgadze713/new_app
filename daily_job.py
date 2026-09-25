from database import SessionLocal
from models import Series
from sync_series import refresh_series
from check_notifications import run_notification_check

def run_daily_job():
    db = SessionLocal()
    all_series = db.query(Series).all()

    total_added = 0
    for series in all_series:
        total_added += refresh_series(series.id)
    sent = run_notification_check()
    return total_added, sent

if __name__ == "__main__":
    added, sent = run_daily_job()
    print("Books added:", added)
    print("Emails sent:", sent)
