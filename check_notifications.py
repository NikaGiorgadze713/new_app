from database import SessionLocal
from models import UserSeries
from models import BookRelease
from models import User
from email_service import send_email


def run_notification_check():

    db = SessionLocal()
    all_rows = db.query(UserSeries).all()
    sent = 0

    for link in all_rows:
        latest_book = (
            db.query(BookRelease)
            .filter(BookRelease.series_id == link.series_id)
            .order_by(BookRelease.book_number.desc())
            .first()
        )

        if latest_book is None:
            continue

        if latest_book.book_number > (link.last_notified_book or 0) and latest_book.book_number > (link.current_book or 0):
            sent += 1
            user = db.query(User).filter(User.id == link.user_id).first()
            send_email(
                user.email,
                "New book in your series!",
                f"Good news! {latest_book.title} (book {latest_book.book_number}) is out.",
            )
            link.last_notified_book = latest_book.book_number

    db.commit()
    return sent


if __name__ == "__main__":
    print("Emails sent:", run_notification_check())
