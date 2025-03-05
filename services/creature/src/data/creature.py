from src.data.init import get_db
from src.model.creature import Creature
from error import Missing,Duplicate
from sqlalchemy import exc
from src.data.schemas import CreatureBase

def get_all() -> list[CreatureBase]:
    db = next(get_db())
    return db.query(Creature).all()

def get_one(name: str) -> CreatureBase:
    db = next(get_db())
    row = db.query(Creature).filter(Creature.name == name).first()
    if row:
        return row
    else:
        raise Missing(msg=f"Creature {name} not found")

def create(creature: CreatureBase) -> CreatureBase:
    if not creature: return None
    db_item = Creature(name = creature.name, country = creature.country, area = creature.area, description = creature.description,
                aka = creature.aka, explorer_id = creature.explorer_id)
    db = next(get_db())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.name)
    except exc.IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exists")

def modify(creature_id: str, creature: CreatureBase) -> CreatureBase:
    if not (creature_id and creature): return None
    db = next(get_db())
    item = db.query(Creature).filter(Creature.id == int(creature_id)).one_or_none()
    if item:
        for var, value in vars(creature).items():
            setattr(item, var, value) if value else None
        db.add(item)
        db.commit()
        db.refresh(item)
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {creature.name} not found")

def delete(creature_id: str):
    if not creature_id: return False
    db = next(get_db())
    item = db.query(Creature).filter(Creature.id == int(creature_id)).one_or_none()
    if item:
        db.delete(item)
        db.commit()
        return True
    else:
        raise Missing(msg=f"Creature not found")

