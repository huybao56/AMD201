from src.data.schemas import RiderBase
import src.data.rider as data

def get_all() -> list[RiderBase]:
    return data.get_all()

def get_one(name: str) -> RiderBase | None:
    return data.get_one(name)

def create(rider: RiderBase) -> RiderBase:
    return data.create(rider)

def replace (rider: RiderBase) -> RiderBase: 
    return data.modify(rider)

def modify(rider_id: str,rider: RiderBase) -> RiderBase:
    return data.modify(rider_id,rider)

# def delete(rider_id: str) -> bool: 
#     return data.delete(rider_id)

