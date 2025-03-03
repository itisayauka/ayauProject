from pydantic import BaseModel

class BookmarkBase(BaseModel):
    user_id: int
    dorama_id: int

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkResponse(BookmarkBase):
    id: int

    class Config:
        from_attributes = True
