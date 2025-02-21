from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import delete, update
from utils import get_current_user
from schemas import book
import model

router = APIRouter(
    prefix= "/books",
    tags=['Books']
)


@router.get("/", response_model= List[book.baseBook])
async def get_books(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Book))
    books = result.scalars().all()
    return books


@router.get("/byName/{title}", response_model=book.baseBook)
async def get_book(title : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Book).where(model.Book.title == title))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/byISBN/{isbn}", response_model=book.baseBook)
async def get_book(isbn : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Book).where(model.Book.isbn == str(isbn)))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=book.baseBook)
async def create_book(book : book.createBook, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)): 
    new_book = model.Book(
        title=book.title,
        author=book.author,
        edition=book.edition,
        publication=book.publication,
        category=book.category,
        department=book.department,
        quantity=book.quantity,
        available=book.available,
        price=book.price,
        rack_no=book.rack_no,
        isbn=book.isbn
    )
    
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)  # ✅ Fetch latest state from DB
    return new_book


@router.put("/{isbn}", status_code=status.HTTP_202_ACCEPTED, response_model=book.updateBook)
async def update_book(isbn : str ,book : book.updateBook, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    query = (
        update(model.Book)
        .where(model.Book.isbn == isbn)
        .values(edition=book.edition, publication=book.publication, quantity=book.quantity, available=book.available, price=book.price, rack_no=book.rack_no)
    )
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(isbn : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(delete(model.Book).where(model.Book.isbn == isbn))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)