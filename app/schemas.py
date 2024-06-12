"""
This module contains the schemas for the Todo application.
"""

from pydantic import BaseModel


class TodoBase(BaseModel):
    """
    Base class for Todo schema.
    """
    title: str
    description: str


class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo item.
    """


class TodoUpdate(TodoBase):
    """
    Schema for updating an existing Todo item.
    """
    completed: bool


class Todo(TodoBase):
    """
    Schema for representing a Todo item.
    """
    id: int
    completed: bool

    class Config:  # pylint: disable=too-few-public-methods
        """
        Config class for enabling ORM mode.
        """
        orm_mode = True
