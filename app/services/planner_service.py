from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate


class PlanService:
	@staticmethod
	def get_plan(db: Session, plan_id: int) -> Plan:
		return db.query(Plan).filter(Plan.id == plan_id).first()

	@staticmethod
	def get_all_plan(db: Session, skip: int = 0, limit: int = 100) -> list[Plan]:
		return db.query(Plan).offset(skip).limit(limit).all()

	@staticmethod
	def create_plan(db: Session, plan: PlanCreate) -> Plan:
		db_plan = Plan(title=plan.title, description=plan.description)

		try:
			db.add(db_plan)
			db.commit()
			db.refresh(db_plan)
			return db_plan
		except SQLAlchemyError as e:
			raise Exception(f"Failed to create plan: {str(e)}")

	@staticmethod
	def update_plan(db: Session, plan_id: int, plan_update: PlanUpdate) -> Plan | None:
		db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
		if not db_plan:
			return None
		try:
			if plan_update.title is not None:
				db_plan.title = plan_update.title  # type: ignore
			if plan_update.description is not None:
				db_plan.description = plan_update.description  # type: ignore
			if plan_update.is_completed is not None:
				db_plan.is_completed = plan_update.is_completed  # type: ignore

			db.commit()
			db.refresh(db_plan)
			return db_plan
		except SQLAlchemyError as e:
			db.rollback()
			raise Exception(f"Failed to update plan: {str(e)}")
	@staticmethod
	def delete_plan(db: Session, plan_id: int) -> bool:
		db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
		if not db_plan:
			return False
		try:
			db.delete(db_plan)
			db.commit()
			return True
		except SQLAlchemyError as e:
			db.rollback()
			raise Exception(f"Failed to delete plan: {str(e)}")
		 