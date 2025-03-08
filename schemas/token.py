from pydantic import BaseModel


class Token(BaseModel):
    token_type : str
    token : str
    
    
class TokenData(BaseModel):
    username : str
    role : bool
    jobId : str