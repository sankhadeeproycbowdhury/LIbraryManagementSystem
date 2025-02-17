from sqlalchemy import Column, Integer, String, Boolean
from config.database import Base  
from sqlalchemy import text

class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    jobId = Column(String(255), nullable=True)
    role = Column(Boolean, nullable=True, server_default=text('FALSE'))