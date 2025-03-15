from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.data.init import get_db
from src.model.models import History

class HistoryCreate(BaseModel):
    booking_id:int
    user_id:int
    rider_id:int
    status:str
    fare:float
    booking_date:str