from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.data.init import get_db
from src.model.models import User
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Định nghĩa User Model cho Request Body
class UserCreate(BaseModel):
    name: str
    account: str
    password: str  # Lưu mật khẩu trực tiếp
    phone_number: str

class UserLoginRequest(BaseModel):
    account: str
    password: str

user_router = APIRouter()

@user_router.post("/register", summary="User Register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.account == user.account).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Account already exists")

    # Lưu mật khẩu trực tiếp
    new_user = User(
        name=user.name,
        account=user.account,
        password_hash=user.password,  
        phone_number=user.phone_number
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}

@user_router.post("/login", summary="User Login")
async def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.account == data.account).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect account or password")

    # So sánh trực tiếp mật khẩu 
    if user.password_hash != data.password:
        raise HTTPException(status_code=401, detail="Incorrect account or password")

    logger.info(f"User {data.account} logged in successfully")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "user_info": {
            "name": user.name,
            "account": user.account,
            "phone_number": user.phone_number
        }
    }

