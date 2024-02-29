from pydantic import BaseModel


class Item(BaseModel):
    name: str
    color: str

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int
