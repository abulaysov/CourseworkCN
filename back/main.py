import json
import asyncio
import websockets


class WebSocket:

    @classmethod
    async def handler(cls, websocket):
        while True:
            try:
                message = await websocket.recv()
            except websockets.ConnectionClosedOK:
                break
            print(message)
            await websocket.send(json.dumps({"hello": "world"}))

    @classmethod
    async def run_server(cls):
        async with websockets.serve(cls.handler, "localhost", 8001):
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(WebSocket.run_server())
