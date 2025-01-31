import asyncio
import websockets

clients = set()

async def chat_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Получено сообщение: {message}")
            await asyncio.gather(*[client.send(message) for client in clients if client != websocket])
    except websockets.exceptions.ConnectionClosed:
        print("Клиент отключился")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(chat_handler, "localhost", 8765):
        print("Сервер запущен на ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
