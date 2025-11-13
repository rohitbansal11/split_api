from sqlalchemy import Column, Integer, String, Float ,DateTime
from src.database.db import Base
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Two relationships for different user roles in Connect
    connects_as_one = relationship("Connect", foreign_keys="[Connect.user_id_one]", back_populates="user_one")
    connects_as_two = relationship("Connect", foreign_keys="[Connect.user_id_two]", back_populates="user_two")
    group_members = relationship("GroupMember",foreign_keys="[GroupMember.user_id]", back_populates="user")
    activities = relationship("Activity",foreign_keys="[Activity.user_id]", back_populates="user")

