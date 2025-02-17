from sqlalchemy import Column, Integer, String
from src.data.init import Base

class Rider(Base):
    __tablename__ = "rider"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)
    account = Column(String, index=True)
    hash = Column(String, index=True)
    rating = Column(float,index=True)
    phoneNumber = Column(String, index=True)
    vehicleType = Column(String, index=True)
    licensePlate = Column(String, index=True)

