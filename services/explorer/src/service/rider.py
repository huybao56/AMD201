from src.data.schemas import ExplorerBase
import src.data.rider as data

def get_all() -> list[ExplorerBase]:
    return data.get_all()

def get_one(name: str) -> ExplorerBase | None:
    return data.get_one(name)

def create(explorer: ExplorerBase) -> ExplorerBase:
    return data.create(explorer)

def replace (explorer: ExplorerBase) -> ExplorerBase: 
    return data.modify(explorer)

def modify(explorer_id: str,explorer: ExplorerBase) -> ExplorerBase:
    return data.modify(explorer_id,explorer)

def delete(explorer_id: str) -> bool: 
    return data.delete(explorer_id)

