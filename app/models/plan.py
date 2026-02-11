
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Plan(Base):
	__tablename__ = "plans"
	
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False, index=True)
	description = Column(Text)
	created_at = Column(DateTime, default=datetime.now)
	updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	is_completed = Column(Boolean, default=False)
	
	tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")