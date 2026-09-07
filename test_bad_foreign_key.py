from database import SessionLocal
from models import UserSeries

db = SessionLocal()

bad_link = UserSeries(user_id=999, series_id=1, current_book=0)
db.add(bad_link)
db.commit()

print("This should NOT have worked!")