from fastapi import APIRouter, HTTPException
import src.service.creature as service
from error import Duplicate, Missing
from src.data.schemas import CreatureBase

router = APIRouter(prefix = "/creature")

@router.get("")
@router.get("/")
def get_all() -> list [CreatureBase]: 
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> CreatureBase:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: CreatureBase) -> CreatureBase:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{creature_id}")
def modify(creature_id: str, creature: CreatureBase) -> CreatureBase:
    try:
        return service.modify(creature_id, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{creature_id}", status_code=204)
def delete(creature_id: str):
    try:
        return service.delete(creature_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
