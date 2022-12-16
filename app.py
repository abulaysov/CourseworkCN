from flask import render_template, request
import sys
from settings import *


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
