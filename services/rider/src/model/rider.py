from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.data.init import get_db
from src.model.models import Rider  
from pydantic import BaseModel
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiderProducer(BaseModel):
    name: str
    account: str
    password: str  
    phone_number: str
    vehicle_type: str
    license_plate: str
    distance_from_rider: float
    price: float


class RiderCreate(BaseModel):
    name: str
    account: str
    password: str  
    phone_number: str
    vehicle_type: str
    license_plate: str

class RiderLoginRequest(BaseModel):
    account: str
    password: str

rider_router = APIRouter()

@rider_router.post("/register",summary="Rider Register")
async def register(rider: RiderCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registering rider with account: {rider.account}")
        
        # Kiểm tra account
        existing_rider = db.query(Rider).filter(Rider.account == rider.account).first()
        if existing_rider:
            raise HTTPException(status_code=400, detail="Account already exists")

        # Kiểm tra phone_number
        if db.query(Rider).filter(Rider.phone_number == rider.phone_number).first():
            raise HTTPException(status_code=400, detail="Phone number already exists")

        # Kiểm tra license_plate
        if db.query(Rider).filter(Rider.license_plate == rider.license_plate).first():
            raise HTTPException(status_code=400, detail="License plate already exists")

        # Lưu mật khẩu trực tiếp nha mấy ní
        new_rider = Rider(
            name=rider.name,
            account=rider.account,
            password_hash=rider.password,  
            phone_number=rider.phone_number,
            vehicle_type=rider.vehicle_type,
            license_plate=rider.license_plate
        )
        
        db.add(new_rider)
        db.commit()
        db.refresh(new_rider)

        logger.info(f" Rider registered successfully with ID: {new_rider.id}")
        return {"message": "Rider registered successfully", "rider_id": new_rider.id}
    
    except Exception as e:
        db.rollback()
        logger.error(f" Error registering rider: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error registering rider: {str(e)}")



@rider_router.post("/login", summary="Rider Login")
async def rider_login(data: RiderLoginRequest, db: Session = Depends(get_db)):
    rider = db.query(Rider).filter(Rider.account == data.account).first()
    
    if not rider:
        logger.warning(f" Account not found: {data.account}")
        raise HTTPException(status_code=401, detail="Account not found")

    # Kiểm tra mật khẩu 
    if rider.password_hash != data.password:
        logger.warning(f" Incorrect password for account: {data.account}")
        raise HTTPException(status_code=401, detail="Incorrect password")

    logger.info(f"✅ Rider {data.account} logged in successfully")

    return {
        "message": "Login successful",
        "rider_id": rider.id,
        "rider_info": {
            "name": rider.name,
            "account": rider.account,
            "phone_number": rider.phone_number,
            "vehicle_type": rider.vehicle_type if rider.vehicle_type else "Unknown",
            "license_plate": rider.license_plate if rider.license_plate else "Unknown"
        }
    }