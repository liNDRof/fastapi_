import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        async def receive():
            while True:
                message = await websocket.recv()
                print(f"\n[Чат]: {message}")

        async def send():
            while True:
                message = input("Вы: ")
                await websocket.send(message)

        await asyncio.gather(receive(), send())

asyncio.run(chat_client())
