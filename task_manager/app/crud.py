from sqlalchemy import desc
from . import models, schemas


def get_tasks(db, offset: int = 0, limit: int = 10, sort_by: str = None):
    query = db.query(models.Task)
    if sort_by == "priority":
        query = query.order_by(desc(models.Task.priority))
    elif sort_by == "due_date":
        query = query.order_by(models.Task.due_date)
    return query.offset(offset).limit(limit).all()


def create_task(db, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    return
