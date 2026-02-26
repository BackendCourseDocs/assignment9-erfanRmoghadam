from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from database import get_connection
from typing import Optional

class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    author: str = Field(..., min_length=3, max_length=100)
    publisher: str = Field(..., min_length=3, max_length=100)
    image_url: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    image_url: Optional[str] = None

search_cache = {}

app = FastAPI()


@app.post("/create")
def add_book(book: Book):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO books (title, author, publisher, image_url)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (book.title, book.author, book.publisher, book.image_url))

    new_id = cur.fetchone()[0]

    con.commit()
    con.close()

    return {"message": "New book added successfully.","id": new_id}


search_cache = {}

@app.get("/search")
def search_books(q: str = Query(..., min_length=3, max_length=100), page: int = 1, size: int = 3):

    cache_key = f"{q}:{page}:{size}"


    if cache_key in search_cache:
        return {
            "message": "Search completed successfully. (cache)",
            **search_cache[cache_key]
        }

    con = get_connection()
    cur = con.cursor()

    offset = (page - 1) * size

    cur.execute("""
        SELECT id, title, author, publisher, image_url
        FROM books
        WHERE title ILIKE %s
           OR author ILIKE %s
           OR publisher ILIKE %s
        OFFSET %s LIMIT %s;
    """, (f"%{q}%", f"%{q}%", f"%{q}%", offset, size))

    results = cur.fetchall()

    cur.execute("""
        SELECT COUNT(*)
        FROM books
        WHERE title ILIKE %s
           OR author ILIKE %s
           OR publisher ILIKE %s;
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    total = cur.fetchone()[0]

    con.close()

    response = {
        "Total Results": total,
        "page": page,
        "size": size,
        "Results": results
    }

    search_cache[cache_key] = response

    return {"message": "Search completed successfully.", **response}



