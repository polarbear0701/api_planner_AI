from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
	title: str
	description: Optional[str] = None
	status: str = "pending" # pending, in_progress, completed
	priority: str = "medium" # low, medium, high
	due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
	pass

class TaskUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	status: Optional[str] = None # pending, in_progress, completed
	priority: Optional[str] = None # low, medium, high
	due_date: Optional[datetime] = None
	
class TaskResponse(TaskBase):
	id: int
	plan_id: int
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)