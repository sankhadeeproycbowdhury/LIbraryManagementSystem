from pydantic import BaseModel

class userLogin(BaseModel):
    username : str
    password : str
    
    model_config = {"from_attributes": True}
    
    
class userOTP(BaseModel):
    email : str
    name : str
    
    model_config = {"from_attributes": True}