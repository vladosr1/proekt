from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Валідаційна модель користувача
class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2, example="Олена Іваненко")
    email: EmailStr
    city: str

# Список користувачів
users: List[User] = [
    User(id=1, name="Олена Іваненко", email="olena@example.com", city="Київ"),
    User(id=2, name="Андрій Петренко", email="andriy@example.com", city="Львів"),
    User(id=3, name="Марія Коваленко", email="maria@example.com", city="Одеса"),
]

@app.get("/users/", response_model=List[User])
def get_users():
    return users

@app.post("/users/", response_model=User)
def create_user(user: User):
    # Перевірка на дубль по email
    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email вже зареєстрований")

    users.append(user)
    return user
    