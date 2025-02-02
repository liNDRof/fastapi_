from fastapi import APIRouter, WebSocket, FastAPI
import asyncio
from contextlib import asynccontextmanager

router = APIRouter()

clients = []
notifications = []

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)

async def send_notification(message: str):
    notifications.append({"message": message})
    if len(notifications) > 10:
        notifications.pop(0)

    for client in clients:
        await client.send_json(notifications[-1])

@router.get("/notifications")
async def get_notifications():
    return notifications

async def match_updates():
    while True:
        await send_notification("матч колись буде")
        await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(match_updates())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
