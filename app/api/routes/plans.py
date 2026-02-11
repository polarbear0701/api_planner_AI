from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.plan import PlanCreate, PlanDetailResponse, PlanResponse, PlanUpdate
from app.services.planner_service import PlanService


router = APIRouter(prefix="/plans", tags=["Plans"])

@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
	try:
		db_plan = PlanService.create_plan(db=db, plan=plan)
		return db_plan
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
		
@router.get("/{plan_id}", response_model=PlanDetailResponse)
async def get_plan_detail(plan_id: int, db: Session = Depends(get_db)):
	db_plan  =PlanService.get_all_plan(db, plan_id)
	if not db_plan:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
		
@router.get("", response_model=list[PlanResponse])
async def list_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	plans = PlanService.get_all_plan(db=db, skip=skip, limit=limit)
	return plans
	
@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(plan_id: int, plan_update: PlanUpdate, db: Session = Depends(get_db)):
	db_plan = PlanService.update_plan(db=db, plan_id=plan_id, plan_update=plan_update)
	if not db_plan:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
	return db_plan

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(plan_id: int, db: Session = Depends(get_db)):
	success = PlanService.delete_plan(db, plan_id)
	if not success:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
	return None