from pydantic import BaseModel

class WatchlistBase(BaseModel):
    user_id: int
    dorama_id: int

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistResponse(WatchlistBase):
    id: int

    class Config:
        from_attributes = True
