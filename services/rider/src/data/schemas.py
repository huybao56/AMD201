from pydantic import BaseModel

class RiderBase(BaseModel):
    name: str
    vehicleType: str
    licensePlate: str
    rating: float
    status: str

class RiderCreate(RiderBase):
    pass

class Rider(RiderBase):
    id: int

    class Config:
        from_attributes = True
