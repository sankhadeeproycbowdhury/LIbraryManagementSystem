from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from sqlalchemy import text, delete, update
from schemas import user
from utils import hash, get_current_user
import model

router = APIRouter(
    prefix= "/users",
    tags=['Users']
)


@router.get("/", response_model= List[user.baseUser])
async def get_users(db: AsyncSession = Depends(get_db), client : str = Depends(get_current_user)):
    # result = await db.execute(text('SELECT * FROM user'))
    # users = result.mappings().all()
    result = await db.execute(select(model.User))
    users = result.scalars().all()
    return users



@router.get("/{name}", response_model=user.baseUser)
async def get_user(name : str, db: AsyncSession = Depends(get_db), client : str = Depends(get_current_user)):
    # result = await db.execute(text("SELECT * FROM user WHERE id = :id"), {"id": id})
    # user = result.mappings().first()  
    result = await db.execute(select(model.User).where(model.User.username == name))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user.baseUser)
async def create_user(user : user.createUser, db: AsyncSession = Depends(get_db), client : str = Depends(get_current_user)):
    # query = text("INSERT INTO users (username, password, email, jobId) VALUES (:username, :password, :email, :jobId)")
    # await db.execute(query, {"username": user.username, "password": user.password, "email": user.email, "jobId" : user.jobId})
    new_user = model.User(
        username=user.username,
        password=hash(user.password),  
        email=user.email,
        jobId=user.jobId
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # ✅ Fetch latest state from DB
    return new_user



@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=user.baseUser)
async def update_user(user : user.updateUser, db: AsyncSession = Depends(get_db), client : str = Depends(get_current_user)):
    # query = text("UPDATE user SET username = :username, password = :password, email = :email WHERE id = :id")
    # result = await db.execute(query, {"id": user.id, "username": user.username, "password":user.password, "email": user.email})
    query = (
        update(model.User)
        .where(model.User.jobId == user.jobId)
        .values(username=user.username, password= hash(user.password), email=user.email)
    )
    
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(name : str, db: AsyncSession = Depends(get_db), client : str = Depends(get_current_user)):
    # query = text("DELETE FROM user WHERE id = :id")
    # result = await db.execute(query, {"id": id})
    result = await db.execute(delete(model.User).where(model.User.username == name))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)