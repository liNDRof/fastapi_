from fastapi import APIRouter, HTTPException
from models import Team, User
from schemas import TeamPydantic
import json

router = APIRouter()
TEAM_FILE = "teams.json"
USER_FILE = "users.json"


def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return [User(**user) for user in json.load(file)]
    except FileNotFoundError:
        return []


def read_teams():
    try:
        with open(TEAM_FILE, "r") as file:
            return [Team(**team) for team in json.load(file)]
    except FileNotFoundError:
        return []


def write_teams(teams):
    with open(TEAM_FILE, "w") as file:
        json.dump([team.dict() for team in teams], file)


@router.post("/team")
async def create_team(team: TeamPydantic):
    teams = read_teams()
    users = read_users()

    if any(existing_team.name == team.name for existing_team in teams):
        raise HTTPException(status_code=400, detail="Team already exists")

    if not any(user.email == team.teamLead.email for user in users):
        raise HTTPException(status_code=404, detail="Team lead not found")

    new_team = Team(
        name=team.name,
        users=[],
        teamLead=User(**team.teamLead.dict())
    )
    teams.append(new_team)
    write_teams(teams)
    return new_team
