from pydantic import BaseModel
from typing import Optional

class DoramaBase(BaseModel):
    title: str
    genre: str
    rating: float

class DoramaCreate(DoramaBase):
    description: Optional[str] = None

class DoramaResponse(DoramaBase):
    id: int
    description: Optional[str]

    class Config:
        from_attributes = True
