from database import SessionLocal
from models import Series

db = SessionLocal()


new_series = Series(name = "Mistborn", author = "Brandon Sanderson", status = "ongoing")
db.add(new_series)
db.commit()

print("Series added!")