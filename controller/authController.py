from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from sqlalchemy.future import select
from schemas import auth, token
from utils import verify, create_access_token, send_otp, get_current_user
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
    
    token = create_access_token(data={"username" : user.username, "role" : user.role, "jobId" : user.jobId})
    
    return {"token_type" : "bearer", "token" : token}


@router.post('/otp')
async def get_otp(auth : auth.userOTP, client : int = Depends(get_current_user)):
    otp = await send_otp(auth.email, auth.name)
    if otp is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OTP not sent")
    return {"OTP" : otp}


