from pydantic import BaseModel
from datetime import date
from enum import Enum

class IssueStatus(str, Enum):
    ISSUED = "Issued"
    RETURNED = "Returned"
    RENEWED = "Renewed"

       
class createBookIssue(BaseModel):
    book_id : int
    student_id : int
    user_id : int
    
class baseBookIssue(createBookIssue):
    issue_date : date
    status : IssueStatus
    due_date : date
    return_date : date | None = None
    renewal_count: int = 0

class updateBookIssue(baseBookIssue):
    user_id : int 
    return_date : date | None
    renewal_count: int = 0
    due_date : date | None
    status : IssueStatus
    
