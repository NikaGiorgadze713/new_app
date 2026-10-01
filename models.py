from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from datetime import datetime


Base = declarative_base()


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    status = Column(String)
    hardcover_id = Column(Integer)


class BookRelease(Base):
    __tablename__ = "BookRelease"
    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"))
    book_number = Column(Float)
    title = Column(String)
    release_date = Column(Integer)
    cover_url = Column(String)


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    email = Column(String)


class UserSeries(Base):
    __tablename__ = "UserSeries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    series_id = Column(Integer, ForeignKey("series.id"))
    current_book = Column(Float)
    notes = Column(String)
    last_notified_book = Column(Integer, default=0)


class Note(Base):
    __tablename__ = "Note"
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("UserSeries.id"))
    book_number = Column(Float)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.now)