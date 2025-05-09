from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from config.database import Base  
from sqlalchemy import text
import enum


class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    jobId = Column(String(255), nullable=True, unique=True)
    role = Column(Boolean, nullable=True, server_default=text('FALSE'))

    issues = relationship("Issue", back_populates="librarian") 


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
    issue_status = Column(Boolean, default=True)

    issues = relationship("Issue", back_populates="student") 


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

    issues = relationship("Issue", back_populates="book")  



class IssueStatus(enum.Enum):
    ISSUED = "Issued"
    RETURNED = "Returned"
    RENEWED = "Renewed"

def get_due_date():
    """Returns default due date (240 days from today)"""
    return datetime.utcnow().date() + timedelta(days=240)


class Issue(Base):
    __tablename__ = "book_issue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(255), ForeignKey("books.isbn", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(255), ForeignKey("students.studentId", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(255), ForeignKey("users.jobId", ondelete="SET NULL"), nullable=True)

    issue_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False, default=get_due_date)
    return_date = Column(Date, nullable=True, default=None)  
    status = Column(Enum(IssueStatus), nullable=False, default=IssueStatus.ISSUED)
    renewal_count = Column(Integer, nullable=False, default=0)
    reminder_sent = Column(Boolean, default=False)
    
    book = relationship("Book", back_populates="issues")
    student = relationship("Student", back_populates="issues")
    librarian = relationship("User", back_populates="issues")


