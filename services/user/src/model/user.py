from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.data.init import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    account = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)

    bookings = relationship("Booking", back_populates="user")
    statuses = relationship("Status", back_populates="user")
    histories = relationship("History", back_populates="user")
