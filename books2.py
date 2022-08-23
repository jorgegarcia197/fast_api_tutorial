"""books2 API"""
from random import randint
import uuid
from typing import Optional
from fastapi import FastAPI, Request, status, Form, Header
from fastapi.responses import JSONResponse
from schemas.book import Book, NegativeNumberException, BookNoRating


app = FastAPI()

BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
    request: Request, exc: NegativeNumberException
):
    """Exception handler for negative number while fetching books"""
    return JSONResponse(
        status_code=418,
        content={
            "message": f"The number must be positive, you entered {exc.books_to_return}"
        },
    )


@app.post("/book/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    """Login to the book API"""
    return {"username": username, "password": password}


@app.get("/books/auth/{book_id}")
async def get_book_with_auth(
    book_id: uuid.UUID,
    username: str = Header(None),
    password: str = Header(None),
):
    """Get a book with authentication"""
    if username == "FastAPIUser" and password == "test1234":
        return await read_book_by_id(book_id)
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})


@app.post("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    """Read header"""
    return {"random_header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    """Returns all books"""
    if not BOOKS:
        create_book_no_api()
    if books_to_return and books_to_return <= 0:
        raise NegativeNumberException(books_to_return)

    if books_to_return and len(BOOKS) > books_to_return:
        return BOOKS[:books_to_return]
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    """Creates a new book"""
    BOOKS.append(book)
    return book


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: uuid.UUID):
    """Read books and return the book with no rating"""
    for book in BOOKS:
        if book.id == book_id:
            return book
    return JSONResponse(status_code=404, content={"message": "Book not found"})


@app.get("/books/{book_id}")
async def read_book_by_id(book_id: uuid.UUID):
    """Function that returns a book by id"""
    for book in BOOKS:
        if book.id == book_id:
            return book
    return JSONResponse(status_code=404, content={"error": "Book not found"})


@app.put("/books/{book_id}")
async def update_book(book_id: uuid.UUID, book: Book):
    """Function that updates a book"""
    book_ = [x for x in BOOKS if x.id == book_id][0]
    if book:
        book_.title = book.title
        book_.author = book.author
        book_.description = book.description
        book_.rating = book.rating
        return book
    return JSONResponse(status_code=404, content={"error": "Book not found"})


@app.delete("/books/{book_id}")
async def delete_book(book_id: uuid.UUID):
    """Function that deletes a book"""
    book_ = [x for x in BOOKS if x.id == book_id][0]
    BOOKS.remove(book_)
    return JSONResponse(
        status_code=200, content={"message": f"Book with id {book_id} deleted"}
    )


def create_book_no_api():
    """Function that generates a number of books to interact with"""
    for i in range(0, 6):
        BOOKS.append(
            Book(
                id=uuid.uuid4(),
                title=f"Book {i}",
                author=f"Author {i}",
                description=f"Description {i}",
                rating=randint(0, 100),
            )
        )
