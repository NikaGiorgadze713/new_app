from database import SessionLocal
from models import UserSeries


db = SessionLocal()


new_followseries = UserSeries(user_id = 1, series_id = 1, current_book = 0)

db.add(new_followseries)
db.commit()

print("followseries added!")