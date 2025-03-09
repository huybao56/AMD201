from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
import random
import logging
from src.model.rider import Rider
from src.model.models import Booking
from src.model.history import History
from pydantic import BaseModel
from src.data.init import get_db

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bảng khoảng cách giả lập
DISTANCE_TABLE = {
    (1, 1): 8, (1, 2): 5, (1, 3): 6, (1, 4): 2, (1, 5): 7,
    (2, 1): 3, (2, 2): 9, (2, 3): 4, (2, 4): 6, (2, 5): 1,
    (3, 1): 5, (3, 2): 2, (3, 3): 8, (3, 4): 7, (3, 5): 4,
    (4, 1): 6, (4, 2): 10, (4, 3): 3, (4, 4): 1, (4, 5): 9,
    (5, 1): 7, (5, 2): 4, (5, 3): 2, (5, 4): 9, (5, 5): 5
}

class BookingRequest(BaseModel):
    user_id: int
    pickup_location: str
    dropoff_location: str
    payment_method: str

booking_router = APIRouter()

def get_distance_from_rider_to_user(user_id: int, rider_id: int) -> float:
    """Lấy khoảng cách từ rider đến user theo bảng giả lập."""
    return DISTANCE_TABLE.get((user_id, rider_id), float('inf'))

def find_closest_available_rider(db: Session, user_id: int):
    """Tìm rider gần nhất có trạng thái available."""
    available_riders = db.query(Rider).filter(Rider.status == "available").all()
    
    if not available_riders:
        return None

    # Sắp xếp rider theo khoảng cách từ bảng DISTANCE_TABLE
    closest_riders = sorted(available_riders, key=lambda r: get_distance_from_rider_to_user(user_id, r.id))
    min_distance = get_distance_from_rider_to_user(user_id, closest_riders[0].id)

    # Chọn tất cả các rider có cùng khoảng cách gần nhất
    filtered_riders = [r for r in closest_riders if get_distance_from_rider_to_user(user_id, r.id) == min_distance]

    return random.choice(filtered_riders) if filtered_riders else None

@booking_router.post("/create")
async def create_booking(data: BookingRequest, db: Session = Depends(get_db)):
    rider = find_closest_available_rider(db, data.user_id)
    if not rider:
        raise HTTPException(status_code=400, detail="No available rider nearby")

    try:
        # Khoảng cách từ rider đến user (dựa vào bảng)
        distance_from_rider_to_you = get_distance_from_rider_to_user(data.user_id, rider.id)

        # Khoảng cách từ điểm đón đến điểm trả (random 1-15 km)
        distance_km = round(random.uniform(1, 15), 2)
        price_per_km = 5.0
        price = round(distance_km * price_per_km, 2)

        new_booking = Booking(
            user_id=data.user_id,
            rider_id=rider.id,
            pickup_location=data.pickup_location,
            dropoff_location=data.dropoff_location,
            payment_method=data.payment_method,
            distance_km=distance_km,  # Khoảng cách từ điểm đón đến điểm trả
            price=price,
            status="pending",
            created_at=datetime.utcnow()
        )

        rider.status = "busy"
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        new_history = History(
            booking_id=new_booking.id,
            user_id=data.user_id,
            rider_id=rider.id,
            status="completed",
            fare=price,
            booking_date=date.today()
        )

        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        logger.info(f"Booking created with ID: {new_booking.id}, Rider ID: {rider.id}")
        return {
            "message": "Booking created successfully",
            "booking_id": new_booking.id,
            "rider_id": rider.id,
            "distance_km": distance_km,  # Khoảng cách từ điểm đón đến điểm trả (dùng để tính giá)
            "distance_from_rider_to_you": distance_from_rider_to_you,  # Khoảng cách từ rider đến user
            "price": price
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
