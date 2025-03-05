from pydantic import BaseModel

class ExplorerBase(BaseModel):
    name: str
    country: str
    description: str

class ExplorerCreate(ExplorerBase):
    pass

class Explorer(ExplorerBase):
    id: int

    class Config:
        from_attributes = True
