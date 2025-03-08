from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import update, or_
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

