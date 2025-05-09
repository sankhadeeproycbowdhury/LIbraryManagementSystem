
from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import delete, update, func, or_, select
from utils import get_current_user
from schemas import student, bookIssue
import datetime as dt
import model

router = APIRouter(
    prefix= "/admin",
    tags=['Admin']
)

@router.get("/revokedStudents", response_model= List[student.baseStudent])
async def get_revoked_students(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    result = await db.execute(select(model.Student).where(model.Student.issue_status == False))
    students = result.scalars().all()
    return students


@router.get("/revokedStudent/{rollNo}", response_model=student.baseStudent)
async def get_revoked_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    result = await db.execute(select(model.Student).where(model.Student.studentId == rollNo))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/overdueIssues", response_model=List[bookIssue.baseBookIssue])
async def get_all_overdue_issues(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    query = select(model.Issue).where(
        model.Issue.status != "Returned",
        model.Issue.due_date > dt.date.today()
    )
    
    result = await db.execute(query)
    issues = result.scalars().all()
    return issues


@router.get("/overdueIssues/{rollNo}", response_model=List[bookIssue.baseBookIssue])
async def get_overdue_issues(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    query = select(model.Issue).where(
        model.Issue.student_id == rollNo,
        model.Issue.status != "Returned",
        model.Issue.due_date > dt.date.today()
    )
    
    result = await db.execute(query)
    issues = result.scalars().all()
    return issues


@router.get("/issuedToday")
async def get_issued_books_today(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    query = (select(model.Book.title, model.Book.author, model.Book.available, model.Book.department, model.Book.category).
            join(model.Issue, model.Book.isbn == model.Issue.book_id).
            where(model.Issue.issue_date == dt.date.today()))
    
    result = await db.execute(query)
    books = result.all()
    
    books_list = [
        {
            "title": row[0],
            "author": row[1],
            "available": row[2],
            "department": row[3],
            "category": row[4]
        }
        for row in books
    ]
    return books_list


@router.get("/issuedBooks")
async def get_issued_books(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    query = (select(model.Book.title, model.Book.author, func.count(model.Issue.book_id).label("borrow_count"), model.Book.available, model.Book.department, model.Book.category).
            join(model.Issue, model.Book.isbn == model.Issue.book_id)
            .group_by(model.Book.isbn)
            .order_by(func.count(model.Issue.book_id).desc()))
    
    result = await db.execute(query)
    books = result.all()
    
    books_list = [
        {
            "title": row[0],
            "author": row[1],
            "borrow_count": row[2],
            "available": row[3],
            "department": row[4],
            "category": row[5]
        }
        for row in books
    ]
    return books_list


@router.get("/issuedBooks/departmentWise")
async def get_issued_books_per_department(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    query = (
        select(
            model.Book.department,
            func.count(model.Issue.book_id).label("issued_count")
        )
        .join(model.Book, model.Book.isbn == model.Issue.book_id)
        .where(or_(model.Issue.status == "Issued", model.Issue.status == "Renewed"))
        .group_by(model.Book.department)
    )

    result = await db.execute(query)
    issues = result.all()

    return [
        {"department": row[0], "issued_count": row[1]}
        for row in issues
    ]



@router.get("/booksByCategory")
async def get_issues_today(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    query = (select(func.count(model.Book.isbn).label("count"), model.Book.category)
            .select_from(model.Book)
            .group_by(model.Book.category))
    
    result = await db.execute(query)
    books = result.all()
    
    books_list = [
        {
            "count": row[0],
            "category": row[1]
        }
        for row in books
    ]
    return books_list


@router.get("/dailyBookIssues")
async def get_daily_book_issues(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):   
    query = (select(func.count(model.Issue.book_id).label("count"), model.Issue.issue_date)
            .select_from(model.Issue)
            .group_by(model.Issue.issue_date))
    
    result = await db.execute(query)
    issues = result.all()
    
    issues_list = [
        {
            "count": row[0],
            "date": row[1]
        }
        for row in issues
    ]
    return issues_list
    


@router.get("/activeStudents")
async def get_active_students(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    query = (select(
            model.Student.firstName, 
            model.Student.studentId, 
            model.Student.department, 
            model.Student.batch, 
            func.count(model.Issue.book_id).label("books_issued"), 
            model.Student.issue_status)
        .join(model.Issue, model.Student.studentId == model.Issue.student_id)
        .group_by(
            model.Student.studentId, 
            model.Student.firstName, 
            model.Student.department, 
            model.Student.batch, 
            model.Student.issue_status)
        .order_by(func.count(model.Issue.book_id).desc()) 
    )

    result = await db.execute(query)
    students = result.all()  

    students_list = [
        {
            "name": row[0],
            "rollNo": row[1],
            "department": row[2],
            "batch": row[3],
            "books_issued": row[4], 
            "issue_status": row[5]  
        }
        for row in students
    ]
    
    return students_list



@router.put("/unrevokedStudent/{rollNo}", status_code=status.HTTP_202_ACCEPTED, response_model=student.baseStudent)
async def unrevoke_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Student).where(model.Student.studentId == rollNo))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.issue_status = True
    await db.commit()
    await db.refresh(student) 
    return student

