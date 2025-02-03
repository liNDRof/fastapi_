from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

router = APIRouter()

connected_clients = []
notifications = []

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def send_notification(message: str):
    notification = {"message": message}
    notifications.append(notification)
    if len(notifications) > 10:
        notifications.pop(0)

    for client in connected_clients:
        await client.send_json(notification)

@router.get("/notifications")
async def get_notifications():
    return {"notifications": notifications}

async def generate_match_updates():
    while True:
        await send_notification("матч")
        await asyncio.sleep(10)

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_match_updates())
