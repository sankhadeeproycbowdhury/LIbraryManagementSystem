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
    
    
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    studentId = Column(String(255), nullable=False, unique=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    batch = Column(Integer, nullable=False)
    
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    edition = Column(String(255), nullable=False)
    publication = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    rack_no = Column(String(255), nullable=False)
    
