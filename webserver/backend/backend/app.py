import os
import sys
from flask import Flask, send_from_directory
from backend.controller.controller import Controller
from backend.settings import set_all


PORT = 8080

app = Flask(__name__)
controller = Controller()


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static/', path)


@app.route('/')
@app.route('/pupper')
@app.route('/settings')
@app.route('/dance')
@app.route('/walk')
@app.route('/jump')
def root():
    return send_from_directory("%s%s" % (os.path.dirname(__file__), '/static/'), 'index.html')

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory("%s%s" % (os.path.dirname(__file__), '/img/'), path)

@app.route("/pupper/<string:command>/<string:param>", methods=['GET'])
def pupper(command, param):
    gait = 'pupper'
    controller.setParams(gait, command, param)
    return controller.getParams(gait, command, param)

@app.route("/settings/<string:command>/<string:param>", methods=['GET'])
def settings(command, param):
    return set_all.exe_setting(command, param)

@app.route("/dance/<string:command>/<string:param>", methods=['GET'])
def dance(command, param):
    gait = 'dance'
    controller.setParams(gait, command, param)
    return controller.getParams(gait, command, param)

@app.route("/walk/<string:command>/<string:param>", methods=['GET'])
def walk(command, param):
    gait = 'walk'
    controller.setParams(gait, command, param)
    return controller.getParams(gait, command, param)

@app.route("/jump/<string:command>/<string:param>", methods=['GET'])
def jump(command, param):
    gait = 'jump'
    controller.setParams(gait, command, param)
    return controller.getParams(gait, command, param)


def main():
    app.run(host='0.0.0.0', port=PORT)


if __name__ == "__main__":
    main()
