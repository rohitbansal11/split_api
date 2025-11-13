from pydantic import BaseModel
from datetime import datetime

class ActivityCreate(BaseModel):
    group_id: str
    name: str
    user_id: str

class Activity(BaseModel):
    id: str
    group_id: str
    name: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True