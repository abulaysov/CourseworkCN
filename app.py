from flask import render_template, request
import sys
from settings import *


@app.route('/', methods=['GET'])
def index():
    """Функция роутер - используется для обработки запроса по адресу '/'
    Обрабатываем только GET запрос"""
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    """Если передать аргумент при запуске приложение, то port и ip будут запущены на нем.
    Иначе запускаем по дефолту на 0.0.0.0 и порт 5000"""
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host='0.0.0.0', port='5000')
