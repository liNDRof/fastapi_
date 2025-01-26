import re
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import List


class User(BaseModel):
    name: str
    email: EmailStr
    passwort: str

    @field_validator("passwort")
    @classmethod
    def passwort_validator(cls, value: str):
        if not re.fullmatch(r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{9,}$', value):
            raise ValueError("Пароль повинен містити мінімум 9 символів, включаючи цифри та спеціальні символи.")
        return value


class Team(BaseModel):
    name: str
    users: List[User]
    teamLead: User


class Tournament(BaseModel):
    name: str
    teams: List[Team]
    winner: Team
    losers: List[Team]

    @model_validator(mode="before")
    @classmethod
    def check_all(cls, values):
        teams = values.get("teams", [])
        losers = values.get("losers", [])
        if len(losers) >= len(teams):
            raise ValueError("Забагато команд у списку програвших!")
        return values

    @model_validator(mode="before")
    @classmethod
    def validate_unique_names(cls, values):
        teams = values.get("teams", [])

        team_names = [team.name for team in teams]
        if len(team_names) != len(set(team_names)):
            raise ValueError("Імена команд повинні бути унікальними.")

        all_users = [user.name for team in teams for user in team.users]
        if len(all_users) != len(set(all_users)):
            raise ValueError("Імена учасників команд повинні бути унікальними.")

        return values
