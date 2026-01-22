from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

count_of_users = 0 
list_of_users = []

class User(BaseModel):
    user_id : int 
    username : str
    age : int

@app.post("/contacts")
def create_contact(user : User) -> list:
    list_of_users.append(user)
    return list_of_users

