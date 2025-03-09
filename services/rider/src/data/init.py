from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = 'postgres'
password = '1'
host = 'localhost'
port = '5432'
database = 'postgres'
connection_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_str)
# import os
# dbUrl = os.environ['DATABASE_URL']
# engine = create_engine(dbUrl)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    from src.model.rider import Rider
    Base.metadata.create_all(bind=engine)
