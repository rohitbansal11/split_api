from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class GroupCreate(BaseModel): # request schema
    name: str
    type: str

class GroupMemberCreate(BaseModel): # request schema
    group_id: str
    user_id: str    

class GroupMember(BaseModel): # response schema
    id: str
    group_id: str
    user_id: str
    split_between_group_member: List[dict]
    # Optional nested relationships - remove if not needed in response
    # group: Optional["Group"] = None
    # user: Optional["User"] = None
    
    class Config:
        from_attributes = True

class Group(BaseModel): # response schema   
    id: str
    name: str
    type: str
    created_at: datetime
    updated_at: datetime
    members: List[GroupMember] = []

    class Config:
        from_attributes = True

# Import User schema and update forward references if needed
try:
    from src.user.scheema import User
    
    # Update GroupMember to include User if you want nested user data
    # This is done after User is imported to avoid circular imports
    if hasattr(GroupMember, 'model_rebuild'):
        GroupMember.model_rebuild()
    if hasattr(Group, 'model_rebuild'):
        Group.model_rebuild()
except ImportError:
    pass  # User schema might not be available