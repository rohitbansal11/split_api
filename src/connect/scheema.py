from pydantic import BaseModel
from datetime import datetime

class ConnectCreate(BaseModel):
    user_id_two: str
    device_name: str

class Connect(BaseModel):
    id: str
    user_id_one: str
    user_id_two: str
    device_name: str
    connected_at: datetime

    class Config:
        from_attributes = True