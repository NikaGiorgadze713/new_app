from database import SessionLocal
from models import UserSeries

db = SessionLocal()


all_links = db.query(UserSeries).all()


for link in all_links:
    print(link.id, link.user_id, link.series_id, link.current_book, link.notes)

    