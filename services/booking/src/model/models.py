from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float,Date
from sqlalchemy.orm import relationship
from datetime import datetime
from src.data.init import Base
import random  # Thêm import random

# 📌 Bảng User
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    account = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)

    bookings = relationship("Booking", back_populates="user")
    histories = relationship("History", back_populates="user")

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

    bookings = relationship("Booking", back_populates="rider")
    histories = relationship("History", back_populates="rider")

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=True)
    pickup_location = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, nullable=True)
    payment_method = Column(String, nullable=True)
    distance_km = Column(Float, nullable=True)

    user = relationship("User", back_populates="bookings")
    rider = relationship("Rider", back_populates="bookings")
    history = relationship("History", back_populates="booking")  

    def calculate_price(self):
        distance_km = random.uniform(2, 15)
        price_per_km = 5.0
        self.price = round(distance_km * price_per_km, 2)
        self.distance_km = distance_km


class History(Base):
    __tablename__ = "history"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=False)
    status = Column(String, nullable=False)  # Completed, Canceled, etc.
    fare = Column(Float, nullable=False)  # Giá tiền của chuyến đi
    booking_date = Column(Date, default=datetime.today)  # Ngày đặt chuyến đi

    # Relationships
    booking = relationship("Booking", back_populates="history")
    user = relationship("User", back_populates="histories")  # Thêm back_populates
    rider = relationship("Rider", back_populates="histories")  # Thêm back_populates