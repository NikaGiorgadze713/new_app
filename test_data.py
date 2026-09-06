from database import SessionLocal
from models import Book
db = SessionLocal()
new_book = Book(title="Mistborn", author="Brandon Sanderson")
db.add(new_book)
db.commit()