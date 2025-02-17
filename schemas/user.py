from pydantic import BaseModel, EmailStr

class baseUser(BaseModel):
    username : str
    email : EmailStr
    jobId : str
    
    model_config = {"from_attributes": True}
    

class createUser(baseUser):
    password : str
    
    
class updateUser(createUser):
    pass