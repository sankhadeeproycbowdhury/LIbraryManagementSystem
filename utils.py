from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from schemas.token import TokenData
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# openssl rand -hex 32
SECRET_KEY = "b53193ccfd204ed45ce7cc1be408b75a132207018bf52f796747be6b39c7a130"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password : str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
 

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('username')
        role : bool = payload.get('role')
        
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username = username, role = role) 
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
    
def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Aceess Token",headers= {"WWW-Authenticate" : "Bearer"})
    # TODO
    # work here and use this method later to check user permissions and authorization
    return verify_access_token(token, credentials_exception)