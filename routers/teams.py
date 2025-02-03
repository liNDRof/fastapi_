from fastapi import APIRouter, HTTPException
from models import Team, User
from schemas import TeamPydantic
import json

router = APIRouter()
TEAM_FILE = "teams.json"
USER_FILE = "users.json"


def read_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


@router.post("/team")
async def create_team(team: TeamPydantic):
    teams = read_json(TEAM_FILE)
    users = read_json(USER_FILE)

    if any(t["name"] == team.name for t in teams):
        raise HTTPException(status_code=400, detail="Тіма вже існує")

    if not any(u["email"] == team.teamLead.email for u in users):
        raise HTTPException(status_code=404, detail="Лідера тіми не знайдено")

    new_team = {
        "name": team.name,
        "users": [],
        "teamLead": {
            "id": team.teamLead.id,
            "name": team.teamLead.name,
            "email": team.teamLead.email
        }
    }

    teams.append(new_team)
    write_json(TEAM_FILE, teams)
    return new_team
