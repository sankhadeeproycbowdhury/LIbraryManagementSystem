from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import delete, update
from utils import get_current_user
from schemas import student
import model


router = APIRouter(
    prefix= "/students",
    tags=['Students']
)


@router.get("/", response_model= List[student.baseStudent])
async def get_students(db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Student))
    students = result.scalars().all()
    return students


@router.get("/{name}", response_model=student.baseStudent)
async def get_student(name : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Student).where(model.Student.firstName == name))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student



@router.get("/{rollNo}", response_model=student.baseStudent)
async def get_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(select(model.Student).where(model.Student.studentId == rollNo))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=student.baseStudent)
async def create_student(student : student.createStudent, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    new_student = model.Student(
        firstName=student.firstName,
        lastName=student.lastName,
        email=student.email,
        phone=student.phone,
        department=student.department,
        batch=student.batch,
        studentId=student.studentId
    )
    
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)  # ✅ Fetch latest state from DB
    return new_student


@router.put("/{rollNo}", status_code=status.HTTP_202_ACCEPTED, response_model=student.updateStudent)
async def update_student(rollNo : str ,student : student.updateStudent, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):    
    query = (
        update(model.Student)
        .where(model.Student.studentId == rollNo)
        .values(firstName=student.firstName, lastName=student.lastName, email=student.email, phone=student.phone, department=student.department)
    )
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{rollNo}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(rollNo : str, db: AsyncSession = Depends(get_db), client : int = Depends(get_current_user)):
    result = await db.execute(delete(model.Student).where(model.Student.studentId == rollNo))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)