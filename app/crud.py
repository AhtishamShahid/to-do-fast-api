"""
This module contains CRUD operations for the Todo application.
"""

from sqlalchemy.orm import Session
from . import models, schemas


def get_todo(db: Session, todo_id: int):
    """
    Retrieve a todo item by its ID.
    """
    return db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate):
    """
    Create a new todo item.
    """
    db_todo = models.TodoItem(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    """
    Update an existing todo item.
    """
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if db_todo is None:
        return None
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    """
    Delete a todo item by its ID.
    """
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}
