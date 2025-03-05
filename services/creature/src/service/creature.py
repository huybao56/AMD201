from src.data.schemas import CreatureBase
import src.data.creature as data

def get_all() -> list[CreatureBase]:
    return data.get_all()

def get_one(name: str) -> CreatureBase | None:
    return data.get_one(name)

def create(creature: CreatureBase) -> CreatureBase:
    return data.create(creature)

def replace (creature_id: str, creature: CreatureBase) -> CreatureBase: 
    return data.modify(creature_id,creature)

def modify(creature_id: str,creature: CreatureBase) -> CreatureBase:
    return data.modify(creature_id,creature)

def delete(creature_id: str) -> bool: 
    return data.delete(creature_id)

