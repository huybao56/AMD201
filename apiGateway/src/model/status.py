from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.model import rider, user
from src.data.init import Base

class User(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(user)
    rider_id = Column(Integer, ForeignKey('rider.id'))
    rider = relationship(rider)
    statusRide = Column(String, index=True)
