from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.models.task import Task
from app.schemas.plan import PlanCreate, PlanUpdate
from app.schemas.task import TaskCreate, TaskUpdate


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
		 
class TaskService:
	@staticmethod
	def get_task(db: Session, task_id: int) -> Task:
		return db.query(Task).filter(Task.id == task_id).first()
	
	@staticmethod
	def get_tasks_by_plan(db: Session, plan_id: int, skip: int = 0, limit: int = 10) -> list[Task]:
		return db.query(Task).filter(Task.plan_id == plan_id).offset(skip).limit(limit).all()
	
	@staticmethod
	def create_task(db: Session, plan_id: int, task: TaskCreate) -> Task:
		db_task = Task(
			plan_id = plan_id,
			title = task.title,
			description = task.description,
			status = task.status,
			priority = task.priority,
			due_date = task.due_date
		)
		
		try:
			db.add(db_task)
			db.commit()
			db.refresh(db_task)
			return db_task
		except SQLAlchemyError as e:
			db.rollback()
			raise Exception(f"Failed to create task: {str(e)}")
	
	@staticmethod
	def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
		db_task = db.query(Task).filter(Task.id == task_id).first()
		if not db_task:
			return None
		try:
			if task_update.title is not None:
				db_task.title = task_update.title  # type: ignore
			if task_update.description is not None:
				db_task.description = task_update.description  # type: ignore
			if task_update.status is not None:
				db_task.status = task_update.status  # type: ignore
			if task_update.priority is not None:
				db_task.priority = task_update.priority  # type: ignore
			if task_update.due_date is not None:
				db_task.due_date = task_update.due_date  # type: ignore

			db.commit()
			db.refresh(db_task)
			return db_task
		except SQLAlchemyError as e:
			db.rollback()
			raise Exception(f"Failed to update task: {str(e)}")
			
	@staticmethod
	def delete_task(db: Session, task_id: int) -> bool:
		db_task = db.query(Task).filter(Task.id == task_id).first()
		if not db_task:
			return False
		try:
			db.delete(db_task)
			db.commit()
			return True
		except SQLAlchemyError as e:
			db.rollback()
			raise Exception(f"Failed to delete task: {str(e)}")