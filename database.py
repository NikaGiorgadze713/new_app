from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
engine = create_engine("sqlite:///books.db")
SessionLocal = sessionmaker(bind=engine)



from models import Base


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


    
Base.metadata.create_all(engine)

