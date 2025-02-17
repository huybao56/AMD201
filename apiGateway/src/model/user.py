from sqlalchemy import Column, Integer, String
from src.data.init import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)
    account = Column(String, index=True)
    hash = Column(String, index=True)
    phoneNumber = Column(String, index=True)

