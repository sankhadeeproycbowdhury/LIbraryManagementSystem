from typing import Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum

class IssueStatus(str, Enum):
    ISSUED = "Issued"
    RETURNED = "Returned"
    RENEWED = "Renewed"

       
class createBookIssue(BaseModel):
    book_id : str
    student_id : str
    
class baseBookIssue(createBookIssue):
    id : int
    user_id : str
    issue_date : date
    status : IssueStatus
    due_date : date
    return_date: Optional[date] = None
    renewal_count: int
    reminder_sent : bool

class updateBookIssue(BaseModel):
    student_id : str
    status : IssueStatus
    renewal_count: int = 0
    
