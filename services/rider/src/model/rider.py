from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.data.init import Base

class Rider(Base):
    __tablename__ = "riders"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    account = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rating = Column(Float, index=True, default=5.0)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    vehicle_type = Column(String, index=True, nullable=False)
    license_plate = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="available")
    statuses = relationship("Status", back_populates="rider")
    bookings = relationship("Booking", back_populates="rider")

    histories = relationship("History", back_populates="rider")
