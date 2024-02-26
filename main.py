from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Book
from app.schema import UserCreate, UserUpdate, BookCreate, BookUpdate



app = FastAPI()


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user_by_email(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}")
def update_user_by_email(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user_by_email(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    if (len(books) == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books in database.")
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    return book

@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict()) # unpack the request rather than manually assigning
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated_book = db.query(Book).filter(Book.id == book_id).first()
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    updated_book.title = book.title
    updated_book.author = book.author
    db.commit()
    return {"message": "Book updated successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = db.query(Book).filter(Book.id == book_id).first()
    if not deleted_book:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found.")
    db.delete(deleted_book)
    db.commit()
    return {"message": "Book deleted successfully"}