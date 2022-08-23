"""Books API with FastAPI"""
from enum import Enum
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Clean Code", "author": "Robert C. Martin"},
    "book_2": {"title": "Clean Architecture 0", "author": "Robert C. Martin"},
    "book_3": {"title": "Clean Architecture", "author": "Robert C. Martin"},
    "book_4": {"title": "Clean Architecture 2", "author": "Robert C. Martin"},
    "book_5": {"title": "Clean Architecture 3", "author": "Robert C. Martin"},
}


class DirectionName(str, Enum):
    """Direction Name Class"""

    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    """Read all books

    Args:
        skip_book (Optional[str], optional): The book that you want to skip if any.
        Defaults to None.

    Returns:
        JSON_response: The object containing all the books available
    """
    if skip_book:
        return {"books": [BOOKS[book] for book in BOOKS if book != skip_book]}
    return BOOKS


@app.get("/books/mybook")
async def read_favorite_book():
    """Returns the favorite book

    Returns:
        JSON_Response: My favorite book written by me
    """
    return {"title": "My favorite book", "author": "Me"}


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    """Returns a book by id

    Args:
        book_id (int): The id of the book to return

    Returns:
        JSON_Response: The book with the given id
    """
    return BOOKS[f"book_{book_id}"]


@app.get("/directions/{direction_name}")
async def read_direction(direction_name: DirectionName):
    """Returns a direction by name

    Args:
        direction_name (DirectionName): The name of the direction to return

    Returns:
        JSON_Response: The direction with the given name
    """
    if direction_name == DirectionName.NORTH:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.SOUTH:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.WEST:
        return {"Direction": direction_name, "sub": "Left"}
    else:
        return {"Direction": direction_name, "sub": "Right"}


@app.post("/")
async def create_book(book_title: str, book_author: str):
    """Creates a new book

    Args:
        book_title (str): The title of the book to create
        book_author (str): The author of the book to create

    Returns:
        JSON_response: The book created
    """
    current_book_id = 0
    if not BOOKS:
        current_book_id = 1
    else:
        current_book_id = len(BOOKS) + 1
    BOOKS[f"book_{current_book_id}"] = {"title": book_title, "author": book_author}
    return BOOKS[f"book_{str(current_book_id)}"]


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    """Updates a book by name

    Args:
        book_name (str): The name of the book to update
        book_title (str): The new title of the book to update
        book_author (str): The new author of the book to update

    Returns:
        JSON_Response: The book updated
    """
    book_info = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_info
    return BOOKS[book_name]


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    """Deletes a book by name

    Args:
        book_name (str): The name of the book to delete

    Returns:
        JSON_Response: The book deleted
    """
    BOOKS.pop(book_name)
    return {"message": f"{book_name} deleted"}


@app.get("/books")
async def read_book_by_query(book_title: str):
    """Returns a book by title

    Args:
        book_title (str): The title of the book to return

    Returns:
        JSON_Response: The book with the given title
    """
    return BOOKS[book_title]


@app.delete("/books")
async def delete_book_by_query(book_title: str):
    """Deletes a book by title

    Args:
        book_title (str): The title of the book to delete

    Returns:
        JSON_Response: The book deleted
    """
    BOOKS.pop(book_title)
    return {"message": f"{book_title} deleted"}
