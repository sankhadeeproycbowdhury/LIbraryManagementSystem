from pydantic import BaseModel, EmailStr

class baseBook(BaseModel):
    title : str
    author : str
    edition : str
    publication : str
    category : str
    department : str
    quantity : int
    available : int
    price : int
    rack_no : str
    isbn : str
    
class createBook(baseBook):
    pass

class updateBook(BaseModel):
    edition : str
    publication : str
    quantity : int
    available : int
    price : int
    rack_no : str