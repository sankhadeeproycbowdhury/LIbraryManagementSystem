from pydantic import BaseModel, EmailStr

class baseStudent(BaseModel):
    firstName : str
    lastName : str
    email : EmailStr
    phone : str
    department : str
    
    model_config = {"from_attributes": True}
    
    
class createStudent(baseStudent):
    batch : int
    studentId : str
    
    
class updateStudent(baseStudent):
    pass
