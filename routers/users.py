from fastapi import APIRouter, HTTPException
from models import User
from schemas import UserPydantic
from typing import List
import uuid

router = APIRouter()

users: List[User] = []


@router.post("/user")
async def create_user(user: UserPydantic):
    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        passwort=user.password
    )
    users.append(new_user)
    return new_user


@router.get("/users")
async def get_users():
    return users

@router.get("/user/{user_id}")
async def get_user(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/user/{user_id}")
async def delete_user(user_id: str):
    global users
    users = [u for u in users if u.id != user_id]
    return {"detail": "User deleted"}
