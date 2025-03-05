from sqlalchemy import Column, Integer, String
from src.data.init import Base

class Explorer(Base):
    __tablename__ = "explorer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    description = Column(String, index=True)
