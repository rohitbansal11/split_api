from sqlalchemy import Column, String, Float, ForeignKey ,JSON
from src.database.db import Base
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    group_id = Column(
        String,
        ForeignKey("groups.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    split_between_group_member = Column(MutableList.as_mutable(JSON), nullable=False, default=list)


   # Explicit foreign_keys are fine for clarity
    group = relationship("Group", back_populates="members", foreign_keys=[group_id])
    user = relationship("User", back_populates="group_members", foreign_keys=[user_id])
    expenses = relationship("Expense", back_populates="group_member", foreign_keys="[Expense.group_member_id]",cascade="all, delete-orphan",passive_deletes=True)