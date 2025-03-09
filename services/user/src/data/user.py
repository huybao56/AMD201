from src.data.init import get_db
from src.model.rider import Rider
from error import Missing,Duplicate
from sqlalchemy import exc
from src.data.schemas import RiderBase

def get_all() -> list[RiderBase]:
    db = next(get_db())
    return db.query(Rider).all()

def get_one(name: str) -> RiderBase:
    db = next(get_db())
    row = db.query(Rider).filter(Rider.name == name).first()
    if row:
        return row
    else:
        raise Missing(msg=f"Rider {name} not found")

def create(rider: RiderBase) -> RiderBase:
    if not rider: return None
    db_item = Rider(name = rider.name,vehicleType = rider.vehicleType, licensePlate = rider.licensePlate, rating = rider.rating, status = rider.status)
    db = next(get_db())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.name)
    except exc.IntegrityError:
        raise Duplicate(msg=f"Rider {rider.name} already exists")

def modify(rider_id: str, rider: RiderBase) -> RiderBase:
    if not (rider_id and rider): return None
    db = next(get_db())
    item = db.query(Rider).filter(Rider.id == int(rider_id)).one_or_none()
    if item:
        for var, value in vars(rider).items():
            setattr(item, var, value) if value else None
        db.add(item)
        db.commit()
        db.refresh(item)
        return get_one(rider.name)
    else:
        raise Missing(msg=f"Rider {rider.name} not found")
