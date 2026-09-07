from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    status = Column(String)


class BookRelease(Base):
    __tablename__ = "BookRelease"
    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"))
    book_number = Column(Integer)
    title = Column(String)
    relase_date = Column(Integer)


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    email = Column(String)


class UserSeries(Base):
    __tablename__ = "UserSeries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    series_id = Column(Integer, ForeignKey("series.id"))
    current_book = Column(Integer)
    notes = Column(String)
