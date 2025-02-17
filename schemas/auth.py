from pydantic import BaseModel

class userLogin(BaseModel):
    username : str
    password : str
    
    model_config = {"from_attributes": True}