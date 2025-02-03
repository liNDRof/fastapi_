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
        await send_notification("матч!")
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(match_updates())  # Запускаємо фонову задачу
    yield  # Очікуємо, поки сервер працює
    task.cancel()  # Завершуємо фонову задачу при зупинці сервера

app = FastAPI(lifespan=lifespan)
app.include_router(router)
