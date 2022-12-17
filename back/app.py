import websockets
import asyncio
import aioschedule as schedule

from service import location, weather
from back.helpers import make_response


class WebSocket:
    """Класс для взаимодействия с клиентом по ВебСокетам
    Атрибут:
        _client - словарь клиентов, структура:
            {some_client: [data: data, loc: loc]}"""
    _clients = {}

    @classmethod
    async def set_city_name(cls, ws, message):
        """Метод для установки города клиенту"""
        cls._clients[ws] = {'loc': message}

    @classmethod
    async def set_current_city_name(cls, ws):
        """Метод устанавливает название города клиенту, если он не указывал название города"""
        if cls._clients.get(ws) and cls._clients.get(ws).get('loc'):
            return
        cls._clients[ws] = {'loc': location.Location().get_city_name()}

    @classmethod
    async def handler(cls, websocket):
        """Метод для обработки запросов, при взаимодействии клиента с приложением"""
        while True:
            try:
                message = await websocket.recv()  # Прослушиваем запрос от клиента
                if bool(message) and message != 'Hello':  # Если пользователь ввел название города
                    await cls.set_city_name(websocket, message)
                elif not bool(message) or message == 'Hello':  # Если пользователь не ввел название города
                    await cls.set_current_city_name(websocket)

                data = weather.Weather.get_weather(cls._clients[websocket]['loc'])
                cls._clients[websocket]['data'] = data  # Сохраняем данные о погоде клиента в атрибуте _clients
                await websocket.send(make_response(data))  # Отправляем к клиенту данные о погоде

            except (websockets.ConnectionClosedOK, ValueError):  # В случае если клиент был отключен
                break

    @classmethod
    async def run_server(cls):
        """Метод для запуска сервера
        Метод websockets.serve принимает 3 аргумента:
            1. cls.handler - это обработчик запросов
            2. 0.0.0.0 - адрес сервера
            3. 8001 - порт сервера"""
        async with websockets.serve(cls.handler, "0.0.0.0", 8001):
            await asyncio.Future()  # run forever

    @classmethod
    async def job(cls):
        """Метод "Job" для выполнения определенной работы:
            Обновлять каждые 30 сек. данные о погоде без взаимодействия пользователя"""
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
        """Метод управляющая Job'ой"""
        schedule.every(30).seconds.do(cls.job)
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()  # Создание нового цикла
    loop.create_task(WebSocket.run_server())  # Создание таски для запуска сервера
    loop.run_until_complete(WebSocket.scheduler())  # Запуск Job'ы в одном цикле с сервером
