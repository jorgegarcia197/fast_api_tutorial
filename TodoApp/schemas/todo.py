from typing import Optional

from pydantic import BaseModel, Field


class Todo(BaseModel):
    """Todo model that representes a todo item row in the database"""

    title: str = Field(..., description="title")
    description: Optional[str] = Field(None, description="description")
    priority: int = Field(gt=0, lt=6, description="priority level from 1 to 5")
    completed: bool = Field(..., description="completed")
