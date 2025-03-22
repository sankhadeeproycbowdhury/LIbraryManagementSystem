from pydantic import BaseModel, EmailStr
       
class createStudent(BaseModel):
    firstName : str
    lastName : str
    email : EmailStr
    phone : str
    department : str
    batch : int
    studentId : str
    
    model_config = {"from_attributes": True}
    
class baseStudent(createStudent):
    issue_status : bool
    
class updateStudent(BaseModel):
    firstName : str
    lastName : str
    email : EmailStr
    phone : str
    department : str
