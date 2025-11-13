from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime
from uuid import uuid4


class Group(Base):
    __tablename__ = "groups"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    members = relationship("GroupMember", back_populates="group", foreign_keys="[GroupMember.group_id]" , cascade="all, delete-orphan",passive_deletes=True)
    expenses = relationship("Expense",back_populates="group",foreign_keys="[Expense.group_id]",cascade="all, delete-orphan",passive_deletes=True)
    activities = relationship("Activity", back_populates="group", foreign_keys="[Activity.group_id]", cascade="all, delete-orphan", passive_deletes=True)