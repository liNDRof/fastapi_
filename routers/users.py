from fastapi import APIRouter, HTTPException
from models import User
from schemas import UserPydantic
from typing import List

router = APIRouter()

users: List[User] = []

current_id = 1

@router.post("/user")
async def create_user(user: UserPydantic):
    global current_id

    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="емейл вже зареєстрований")

    new_user = User(
        id=current_id,
        name=user.name,
        email=user.email,
        passwort=user.password
    )

    users.append(new_user)

    current_id += 1

    return new_user

@router.get("/users")
async def get_users():
    return users

@router.get("/user/{user_id}")
async def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="юзера не знайдено")

@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    global users
    users = [u for u in users if u.id != user_id]
    return {"detail": "юзер делітед"}
