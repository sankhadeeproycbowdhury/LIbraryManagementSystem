from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from schemas.token import TokenData
import jwt, smtplib, asyncio, random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.database import get_db
from model import Student, Book, Issue


# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587
EMAIL_SENDER = "12211059cse@gmail.com"
EMAIL_PASSWORD = "aewz nlgs bxlp gxub"

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
        jobId : str = payload.get('jobId')
        
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username = username, role = role, jobId = jobId) 
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
    
def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Aceess Token", headers= {"WWW-Authenticate" : "Bearer"})
    return verify_access_token(token, credentials_exception)
    

async def get_due_students():
    async for db in get_db():
        today = datetime.date.today()
        due_date = today + timedelta(days=2)
        
        query = (select(Student.email, Student.firstName, Book.title, Issue.due_date)
                .join(Issue, Student.studentId == Issue.student_id)
                .join(Book, Issue.book_id == Book.isbn)
                .where(Issue.due_date == due_date))
        
        result = await db.execute(query)
        return result.all()

async def send_email(recipient, student_name, book_title, due_date):
    message = MIMEMultipart()
    message['From'] = EMAIL_SENDER
    message['To'] = recipient
    message['Subject'] = "Library Management System: Due Date Reminder"
    
    body = f"Hello {student_name},\n\nThis is a reminder that you have to return the book '{book_title}' by {due_date}. If you have already returned the book, please ignore this message.\n\nThank you."
    message.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, message.as_string())
        server.quit()
        

async def send_otp(recipient: str, student_name: str) -> int:
    message = MIMEMultipart()
    message['From'] = EMAIL_SENDER
    message['To'] = recipient
    message['Subject'] = "Library Management System: OTP for verification"
    
    otp = random.randint(1000, 9999)
    body = f"Hello {student_name},\n\nThis is your OTP for verification: {otp} \n\n"
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, message.as_string())
            server.quit()
        return otp
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None


        
async def check_and_send_reminders():
    students = await get_due_students()
    for email, firstName, title, due_date in students:
        await send_email(email, firstName, title, due_date)
        print(f"✅ Reminder sent to {firstName} ({email}) for book '{title}' due on {due_date}")
        await asyncio.sleep(1)

    
    
    
    
    
    
