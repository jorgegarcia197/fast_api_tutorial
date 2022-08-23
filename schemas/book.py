from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class BookNoRating(BaseModel):
    """Book with no rating parameter"""

    id: UUID
    title: str = Field(..., description="The title of the book", min_length=1)
    author: str = Field(
        ..., description="The author of the book", min_length=1, max_length=100
    )
    description: Optional[str] = Field(
        None, description="The description of the book", max_length=1000
    )

    class Config:
        """ Example Config class"""
        schema_extra = {
            "example": {
                "id": "d5f8f8c4-e848-4d8e-9c8e-d834cd9f9c5e",
                "title": "The Art of War",
                "author": "Sun Tzu",
                "description": "A book about war",
            }
        }


class Book(BaseModel):
    """Book Class Definition"""

    id: UUID
    title: str = Field(..., description="The title of the book", min_length=1)
    author: str = Field(
        ..., description="The author of the book", min_length=1, max_length=100
    )
    description: Optional[str] = Field(
        None, description="The description of the book", max_length=1000
    )
    rating: int = Field(None, gt=-1, lt=101, description="The rating of the book")

    class Config:
        schema_extra = {
            "example": {
                "id": "d5f8f8c4-e848-4d8e-9c8e-d834cd9f9c5e",
                "title": "The Art of War",
                "author": "Sun Tzu",
                "description": "A book about war",
                "rating": 100,
            }
        }


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return
