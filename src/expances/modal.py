from sqlalchemy import Column, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime
from uuid import uuid4
from sqlalchemy.ext.mutable import MutableList

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    group_id = Column(String, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    group_member_id = Column(String, ForeignKey("group_members.id", ondelete="CASCADE"), nullable=False)
    # Store split info as JSON: [{"user_id": "...", "amount": 123.0}, ...]
    split_between_group_member = Column(MutableList.as_mutable(JSON), nullable=False, default=list)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to group
    group = relationship("Group", back_populates="expenses", foreign_keys=[group_id])
    group_member = relationship("GroupMember", back_populates="expenses", foreign_keys=[group_member_id])