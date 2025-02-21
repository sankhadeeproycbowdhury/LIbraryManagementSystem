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