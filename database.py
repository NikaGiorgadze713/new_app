from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///books.db")
SessionLocal = sessionmaker(bind=engine)



from models import Base

Base.metadata.create_all(engine)