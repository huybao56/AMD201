from fastapi import APIRouter, HTTPException
from src.data.schemas import RiderBase
from src.model.rider import Rider
import src.service.rider as service
from error import Duplicate, Missing

router = APIRouter(prefix = "/rider")


@router.get("/")
def get_all() -> list [RiderBase]: 
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> RiderBase:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(rider: RiderBase) -> RiderBase:
    try:
        return service.create(rider)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{rider_id}")
def modify(rider_id: str, rider: RiderBase) -> RiderBase:
    try:
        return service.modify(rider_id, rider)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

# @router.delete("/{rider_id}", status_code=204)
# def delete(rider_id: str):
#     try:
#         return service.delete(rider_id)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)
