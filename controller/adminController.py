
from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import delete, update
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
    if(client.role == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    result = await db.execute(select(model.Student).where(model.Student.issue_status == False))
    students = result.scalars().all()
    return students


@router.get("/revokedStudent/{rollNo}", response_model=student.baseStudent)
async def get_revoked_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    if(client.role == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    result = await db.execute(select(model.Student).where(model.Student.studentId == rollNo))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/overdueIssues/{rollNO}", response_model=List[bookIssue.baseBookIssue])
async def get_overdue_issues(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    if(client.role == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    query = select(model.Issue).where(
        model.Issue.student_id == rollNo,
        model.Issue.status != "Returned",
        model.Issue.due_date < dt.date.today()
    )
    result = await db.execute(query)
    issues = result.scalars().all()
    return issues


@router.put("/unrevokedStudent/{rollNo}", status_code=status.HTTP_202_ACCEPTED, response_model=student.baseStudent)
async def unrevoke_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    if(client.role == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    result = await db.execute(select(model.Student).where(model.Student.studentId == rollNo))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.issue_status = True
    await db.commit()
    await db.refresh(student) 
    return student

