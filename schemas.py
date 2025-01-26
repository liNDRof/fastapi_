from pydantic import BaseModel, EmailStr
from typing import List

class UserPydantic(BaseModel):
    name: str
    email: EmailStr
    password: str

class TeamPydantic(BaseModel):
    name: str
    teamLead: UserPydantic

class Tournaments(BaseModel):
    name: str
    teams: List[TeamPydantic]
