from database import SessionLocal
from models import UserSeries

db = SessionLocal()

link = db.query(UserSeries).filter(UserSeries.id == 1).first()

link.current_book = 1
link.notes = "Vin discovered she's a Mistborn"

db.commit()
