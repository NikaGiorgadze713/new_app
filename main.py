from hardcover_service import get_series_books, search_series
from hardcover_service import get_series_books
from sync_series import save_series_to_db, clean_book_list, remove_duplicate_positions, refresh_series
from fastapi import FastAPI
from database import SessionLocal
from models import Series
from pydantic import BaseModel
from models import User
from models import UserSeries
from check_notifications import run_notification_check
from fastapi.responses import FileResponse
from models import BookRelease


class SeriesCreate(BaseModel):

    name: str
    author: str


app = FastAPI()


@app.post("/series")
def create_series(series: SeriesCreate):
    db = SessionLocal()
    new_series = Series(
        name=series.name, author=series.author, status="ongoing")
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
    new_user = User(email=users.email)
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
    existing = db.query(UserSeries).filter(
        UserSeries.user_id == request.user_id, UserSeries.series_id == request.series_id,).first()
    if existing is not None:
        return {"message": "Already following this series"}
    else:
        new_link = UserSeries(
            user_id=request.user_id, series_id=request.series_id, current_book=request.current_book)
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
    follow_request = db.query(UserSeries).filter(
        UserSeries.user_id == user_id).all()
    return follow_request


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
    return {"message": "Notification check complete", "emails_sent": sent}


@app.post("/series/{series_id}/refresh")
def refresh_series_endpoint(series_id: int):
    added = refresh_series(series_id)
    return {"message": "Series refreshed", "books_added": added}


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/search")
def search(name: str):
    result = search_series(name)
    hits = result["data"]["search"]["results"]["hits"]

    clean = []

    for hit in hits:
        doc = hit["document"]
        clean.append({"hardcover_id": int(doc["id"]), "name": doc["name"], "author": doc.get(
            "author_name"), "readers": doc.get("readers_count", 0)})
    return clean





class FollowFromSearchRequest(BaseModel):
    user_id: int
    hardcover_id: int
    name: str
    author: str
    current_book: int


class LoginRequest(BaseModel):
    email: str


@app.post("/follow/from-search")
def follow_from_search(request: FollowFromSearchRequest):
    db = SessionLocal()

    series = db.query(Series).filter(Series.hardcover_id == request.hardcover_id).first()

    if series is None:
        result = get_series_books(request.hardcover_id)
        raw_list = result["data"]["series_by_pk"]["book_series"]
        cleaned = clean_book_list(raw_list)
        final = remove_duplicate_positions(cleaned)
        series = save_series_to_db(request.name, request.author, final, request.hardcover_id)

    existing = db.query(UserSeries).filter(
        UserSeries.user_id == request.user_id,
        UserSeries.series_id == series.id,
    ).first()

    if existing is not None:
        return {"message": "Already following this series"}

    new_link = UserSeries(
        user_id=request.user_id,
        series_id=series.id,
        current_book=request.current_book,
    )
    db.add(new_link)
    db.commit()
    return {"message": "Now following series", "series_id": series.id}


@app.get("/my-series/{user_id}")
def my_series(user_id: int):
    db = SessionLocal()
    links = db.query(UserSeries).filter(UserSeries.user_id == user_id).all()

    result = []
    for link in links:
        series = db.query(Series).filter(Series.id == link.series_id).first()
        latest_book = (
            db.query(BookRelease)
            .filter(BookRelease.series_id == link.series_id)
            .order_by(BookRelease.book_number.desc())
            .first()
        )

        result.append({
            "link_id": link.id,
            "series_name": series.name,
            "author": series.author,
            "current_book": link.current_book,
            "notes": link.notes,
            "latest_book_number": latest_book.book_number if latest_book else None,
            "latest_book_title": latest_book.title if latest_book else None,
        })

    return result


@app.post("/login")
def login(request: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == request.email).first()

    if user is None:
        user = User(email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"user_id": user.id, "email": user.email}