from pydantic import BaseModel, EmailStr

class baseStudent(BaseModel):
    firstName : str
    lastName : str
    email : EmailStr
    phone : str
    department : str
    batch : int
    studentId : str
    
    model_config = {"from_attributes": True}
    
    
class createStudent(baseStudent):
    pass
    
    
class updateStudent(BaseModel):
    firstName : str
    lastName : str
    email : EmailStr
    phone : str
    department : str
