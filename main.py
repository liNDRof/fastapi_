from fastapi import FastAPI
from routers import users, teams, tournaments

app = FastAPI()

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(tournaments.router)

@app.get("/")
async def start():
    return {'message': "hello world"}
