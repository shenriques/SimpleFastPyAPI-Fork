from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from .. models import Book
from .. schema import BookCreate, BookUpdate, BookShow
from typing import List

router = APIRouter(prefix="/books", tags=['Books'])

@router.get("/", response_model=List[BookShow])
def get_all_books(db: Session = Depends(get_db)):
    book_objects = db.query(Book).all() # obtain a list of all books in database
    if (len(book_objects) == 0): # if the list is empty, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books in database.")
    books = [BookShow(title=book.title, author=book.author) for book in book_objects] # create a BookShow object for each book in list
    return books

@router.get("/{book_id}", response_model=BookShow)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first() # search for the book by ID
    if not book: # raise a 404 error if book of that ID doesnt exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    open_book = BookShow(title=book.title, author=book.author) # create a BookShow object for the searched book
    return open_book

@router.post("/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict()) # unpack the request rather than manually assigning
    db.add(new_book)
    db.commit() # add new book to database
    db.refresh(new_book) # retrieve the newly created book
    return new_book

@router.put("/{book_id}")
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated_book = db.query(Book).filter(Book.id == book_id).first()
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    updated_book.title = book.title
    updated_book.author = book.author
    db.commit()
    return {"message": "Book updated successfully"}

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = db.query(Book).filter(Book.id == book_id).first()
    if not deleted_book:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    db.delete(deleted_book)
    db.commit()
    return {"message": "Book deleted successfully"}