from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ExpenseCreate(BaseModel): # request schema
    group_id: str
    name: str
    amount: float
    split_between_group_member: List[dict]

class ExpenseEdit(BaseModel): # request schema
    name: str
    amount: float
    split_between_group_member: List[dict]

class Expense(BaseModel): # response schema
    id: str
    group_id: str
    name: str
    amount: float
    group_member_id:str
    split_between_group_member: List[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True