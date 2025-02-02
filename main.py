from fastapi import FastAPI
from routers import users, teams, tournaments, notifications

app = FastAPI()

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(tournaments.router)
app.include_router(notifications.router)

@app.get("/")
async def start():
    return {'message': "hello world"}
