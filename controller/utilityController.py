from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import update, or_, func
from datetime import date, timedelta
from utils import get_current_user
from schemas import bookIssue
import model


router = APIRouter(
    prefix= "/issues",
    tags=['IssueBooks']
)


@router.get("/", response_model= List[bookIssue.baseBookIssue])
async def get_issues(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Issue))
    issues = result.scalars().all()
    return issues


@router.get("/search", response_model= List[bookIssue.baseBookIssue])
async def get_issues(issue : bookIssue.createBookIssue, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    query = select(model.Issue).where(
        model.Issue.student_id == issue.student_id,
        model.Issue.book_id == issue.book_id
    )
    result = await db.execute(query)
    issues = result.scalars().all()
    return issues


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_issue(issue : bookIssue.createBookIssue, db: AsyncSession = Depends(get_db), client : dict = Depends(get_current_user)):
    query = select(model.Issue).where(
        model.Issue.book_id == issue.book_id,
        model.Issue.student_id == issue.student_id,
        or_(model.Issue.status == "Issued", model.Issue.status == "Renewed")
    )
    result = await db.execute(query)
    issue_exists = result.scalars().first()
    if issue_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already issued to the student")
    
    
    count_query = select(func.count()).where(
        model.Issue.student_id == issue.student_id,
        or_(model.Issue.status == "Issued", model.Issue.status == "Renewed")
    )
    count_result = await db.execute(count_query)
    issued_books_count = count_result.scalar()    
    if issued_books_count >= 14:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student has already issued 10 books")

    
    new_issue = model.Issue(
        book_id=issue.book_id,
        student_id=issue.student_id,
        user_id=client.jobId
    )
    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    print(client.jobId)
    return {"message": "Book Issued Successfully"}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_issue(id : int, issue : bookIssue.updateBookIssue, db: AsyncSession = Depends(get_db), client : dict = Depends(get_current_user)):
    query = select(model.Issue).where(model.Issue.id == id)
    result = await db.execute(query)
    issue_exists = result.scalars().first()
            
    if not issue_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    if issue_exists.status.value == bookIssue.IssueStatus.RETURNED.value: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book has already been returned")
    
    update_values = {"status": issue.status, "user_id": client.jobId}
    
    if issue.status == "Returned":
        update_values["return_date"] = date.today() 
    elif issue.status == "Renewed":
        update_values["renewal_count"] = issue_exists.renewal_count + 1 
        update_values["due_date"] = issue_exists.due_date + timedelta(days=30) 

    update_query = update(model.Issue).where(model.Issue.id == id).values(update_values)
    await db.execute(update_query)
    await db.commit()
    return {"message": "Issue updated successfully"}

