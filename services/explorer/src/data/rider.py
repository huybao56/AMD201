from src.data.init import get_db
from src.model.rider import Explorer
from error import Missing,Duplicate
from sqlalchemy import exc
from src.data.schemas import ExplorerBase

def get_all() -> list[ExplorerBase]:
    db = next(get_db())
    return db.query(Explorer).all()

def get_one(name: str) -> ExplorerBase:
    db = next(get_db())
    row = db.query(Explorer).filter(Explorer.name == name).first()
    if row:
        return row
    else:
        raise Missing(msg=f"Explorer {name} not found")

def create(explorer: ExplorerBase) -> ExplorerBase:
    if not explorer: return None
    db_item = Explorer(name = explorer.name, country = explorer.country, description = explorer.description)
    db = next(get_db())
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.name)
    except exc.IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")

def modify(explorer_id: str, explorer: ExplorerBase) -> ExplorerBase:
    if not (explorer_id and explorer): return None
    db = next(get_db())
    item = db.query(Explorer).filter(Explorer.id == int(explorer_id)).one_or_none()
    if item:
        for var, value in vars(explorer).items():
            setattr(item, var, value) if value else None
        db.add(item)
        db.commit()
        db.refresh(item)
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {explorer.name} not found")
