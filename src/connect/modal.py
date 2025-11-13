from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

class Connect(Base):
    __tablename__ = "connects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id_one = Column(String, ForeignKey("users.id"), nullable=False)  # <-- FK to User
    user_id_two = Column(String, ForeignKey("users.id"), nullable=False)  # <-- FK to User
    device_name = Column(String, nullable=False)
    connected_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Define two separate relationships to User
    user_one = relationship("User", foreign_keys=[user_id_one], back_populates="connects_as_one")
    user_two = relationship("User", foreign_keys=[user_id_two], back_populates="connects_as_two")
