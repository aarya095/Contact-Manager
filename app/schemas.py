from pydantic import BaseModel

class Contact(BaseModel):
    name : str
    number : int
    email : str = None
