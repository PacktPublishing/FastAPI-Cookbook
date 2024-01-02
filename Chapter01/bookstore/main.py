from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from models import Book
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
    }


@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    return {
        "author_id": author_id,
        "name": "Ernest Hemingway",
    }


@app.get("/books")
async def read_books(year: int = None):
    if year:
        return {
            "year": year,
            "books": ["Book 1", "Book 2"],
        }
    return {"books": ["All Books"]}


@app.post("/books")
async def create_book(book: Book):
    return book


class BookResponse(BaseModel):
    title: str
    author: str


@app.get("/allbooks", response_model=list[BookResponse])
async def read_all_books():
    return [
        {"title": "1984", "author": "George Orwell"},
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
    ]


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Oops! Something went wrong"},
    )


@app.get("/error_endpoint")
async def raise_excpetion():
    raise HTTPException(status_code=500)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return PlainTextResponse(
        str(exc), status_code=status.HTTP_400_BAD_REQUEST
    )
