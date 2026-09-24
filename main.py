from fastapi import FastAPI
from database import SessionLocal
from models import Series
from pydantic import BaseModel
from models import User
from models import UserSeries
from check_notifications import run_notification_check


class SeriesCreate(BaseModel):


    name: str
    author: str

app = FastAPI()

@app.post("/series")

def create_series(series: SeriesCreate):
    db = SessionLocal()
    new_series = Series(name = series.name, author = series.author, status = "ongoing")
    db.add(new_series)
    db.commit()
    return {"massage": "Series created", "id": new_series.id}



@app.get("/series")

def get_series():

    db = SessionLocal()
    all_series = db.query(Series).all()
    
    return all_series


class UserCreate(BaseModel):
    email: str

@app.post("/user")
def create_user(users: UserCreate):
    db = SessionLocal()
    new_user = User(email = users.email)
    db.add(new_user)
    db.commit()
    return {"massage": "User Created", "id": new_user.id}



@app.get("/user")

def get_user():
    db = SessionLocal()
    all_users = db.query(User).all()

    return all_users

     


class FollowRequest(BaseModel):
    user_id: int
    series_id: int
    current_book: int


@app.post("/follow")
def follow_series(request: FollowRequest):
    db = SessionLocal()
    new_link = UserSeries(user_id=request.user_id, series_id=request.series_id, current_book=request.current_book)
    db.add(new_link)
    db.commit()
    return {"message": "Now following series", "id": new_link.id}


@app.get("/follow")

def get_follow_series():
    db = SessionLocal()
    all_follow_request = db.query(UserSeries).all()

    return all_follow_request



class UpdateProgressRequest(BaseModel):
    current_book: int
    notes: str



@app.put("/follow/{link_id}")

def update_follow(link_id: int, request: UpdateProgressRequest):
    db = SessionLocal()
    link = db.query(UserSeries).filter(UserSeries.id == link_id).first()
    link.current_book = request.current_book
    link.notes = request.notes
    db.commit()
    return {"message": "Progress updated", "current_book": link.current_book, "notes": link.notes}
    



@app.get("/follow/{user_id}")


def see_follow(user_id: int,):
    db = SessionLocal()
    follow_request = db.query(UserSeries).filter(UserSeries.user_id == user_id).all()
    return follow_request




from sync_series import save_series_to_db, clean_book_list, remove_duplicate_positions
from hardcover_service import get_series_books

@app.post("/series/import/{hardcover_id}")
def import_series(hardcover_id: int, name: str, author: str):
    result = get_series_books(hardcover_id)
    raw_list = result["data"]["series_by_pk"]["book_series"]
    cleaned = clean_book_list(raw_list)
    final = remove_duplicate_positions(cleaned)
    save_series_to_db(name, author, final, hardcover_id)
    return {"message": "Series imported", "books_added": len(final)}


@app.post("/notifications/check")
def check_notifications():
    sent = run_notification_check()
    return{"message": "Notification check complete", "emails_sent": sent}