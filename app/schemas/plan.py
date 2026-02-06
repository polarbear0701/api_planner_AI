

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PlanBase(BaseModel):
	title: str
	description: Optional[str] = None
	
class PlanCreate(PlanBase):
	pass

class PlanUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	is_completed: Optional[bool] = None

class PlanResponse(PlanBase):
	id: int
	created_at: datetime
	updated_at: datetime
	is_completed: bool
	
	model_config = ConfigDict(from_attributes=True)
		
class PlanDetailResponse(PlanResponse):
	tasks: List = []