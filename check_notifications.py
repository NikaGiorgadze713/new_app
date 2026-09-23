from database import SessionLocal
from models import  UserSeries
from models import BookRelease


db = SessionLocal()
all_rows = db.query(UserSeries).all()

for link in all_rows:
    latest_book = db.query(BookRelease).filter(BookRelease.series_id == link.series_id).order_by(BookRelease.book_number.desc()).first()

    if latest_book is None:
        continue

    if latest_book.book_number > (link.last_notified_book or 0) and latest_book.book_number > (link.current_book or 0):
        print("Notify user", link.user_id, "about", latest_book.title)
        link.last_notified_book = latest_book.book_number

db.commit()