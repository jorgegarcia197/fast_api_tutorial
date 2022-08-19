from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Clean Code", "author": "Robert C. Martin"},
    "book_2": {"title": "Clean Architecture 0", "author": "Robert C. Martin"},
    "book_3": {"title": "Clean Architecture", "author": "Robert C. Martin"},
    "book_4": {"title": "Clean Architecture 2", "author": "Robert C. Martin"},
    "book_5": {"title": "Clean Architecture 3", "author": "Robert C. Martin"},
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        return {"books": [BOOKS[book] for book in BOOKS if book != skip_book]}
    return BOOKS


@app.get("/{book_id}")
async def read_book(book_id: str):
    return BOOKS[book_id]


@app.get("/books/mybook")
async def read_favorite_book():
    return {"title": "My favorite book", "author": "Me"}


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return BOOKS[f"book_{book_id}"]


@app.get("/directions/{direction_name}")
async def read_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "Left"}
    else:
        return {"Direction": direction_name, "sub": "Right"}


@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0
    if not BOOKS:
        current_book_id = 1
    else:
        current_book_id = len(BOOKS) + 1
    BOOKS[f"book_{current_book_id}"] = {"title": book_title, "author": book_author}
    return BOOKS[f"book_{str(current_book_id)}"]


@app.put("/{book_name}")
async def updatebook(book_name: str, book_title: str, book_author: str):
    book_info = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_info
    return BOOKS[book_name]
