from fastapi import APIRouter, HTTPException
from models import Tournament, Team, User
from schemas import Tournaments
from typing import List

router = APIRouter()

teams: List[Team] = []
tournaments: List[Tournament] = []

@router.post("/tournament")
async def create_tournament(tournament: Tournaments):
    existing_teams = [team for team in teams if team.name in [t.name for t in tournament.teams]]
    if len(existing_teams) != len(tournament.teams):
        raise HTTPException(status_code=400, detail="Some teams not found")

    for team in existing_teams:
        if not any(user.name == team.teamLead.name and user.email == team.teamLead.email for user in team.users):
            raise HTTPException(status_code=404, detail=f"Team lead for team {team.name} not found")

    new_tournament = Tournament(
        name=tournament.name,
        teams=existing_teams,
        winner=None,
        losers=[]
    )
    tournaments.append(new_tournament)
    return new_tournament
