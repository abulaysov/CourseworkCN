import websockets
import asyncio
import aioschedule as schedule

from service import location, weather
from back.helpers import make_response


class WebSocket:
    _clients = {}

    @classmethod
    async def handler(cls, websocket):
        loc = location.Location().get_city_name()
        while True:
            try:
                await websocket.recv()
            except websockets.ConnectionClosedOK:
                break
            data = weather.Weather.get_weather(loc)
            cls._clients[websocket] = {'data': data, 'loc': loc}
            await websocket.send(make_response(data))

    @classmethod
    async def run_server(cls):
        async with websockets.serve(cls.handler, "localhost", 8001):
            await asyncio.Future()  # run forever

    @classmethod
    async def job(cls):
        for ws in cls._clients:
            data = weather.Weather.get_weather(cls._clients[ws]['loc'])
            cls._clients[ws]['data'] = data
            try:
                await ws.send(make_response(data))
            except websockets.ConnectionClosedOK:
                cls._clients.pop(ws)
            await asyncio.sleep(1)

    @classmethod
    async def scheduler(cls):
        schedule.every(30).seconds.do(cls.job)
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(WebSocket.run_server())
    loop.run_until_complete(WebSocket.scheduler())
