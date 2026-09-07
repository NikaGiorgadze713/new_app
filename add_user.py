from database import SessionLocal
from models import User

db = SessionLocal()

new_user = User(email = "testgmail@gmail.com")

db.add(new_user)
db.commit()