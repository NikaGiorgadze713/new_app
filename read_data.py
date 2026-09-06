from database import SessionLocal
from models import Book

db = SessionLocal()
books = db.query(Book).all()

for book in books:
    print(book.id, "-", book.title, "-", book.author)