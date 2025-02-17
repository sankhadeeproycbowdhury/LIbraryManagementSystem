from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from sqlalchemy.future import select
from schemas import auth, token
from utils import verify, create_access_token
import model

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=token.Token)
async def login(userCredentials : OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.User).where(model.User.username == userCredentials.username))
    user = result.scalar_one_or_none()
    if not user or not verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    token = create_access_token(data={"username" : user.username, "role" : user.role})
    
    return {"token_type" : "bearer", "token" : token}

