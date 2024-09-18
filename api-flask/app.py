from datetime import datetime
import json

from flask import Flask, Response
from flask_restful import Resource, Api

from helpers import UPLOAD_FOLDER
from src.image_process.image_process import process_image_manometro

app = Flask(__name__)
api = Api(app)

from src.resources.ManometerRouters import ManometerRouters

api.add_resource(ManometerRouters, '/')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP_CONF_UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

if __name__ == '__main__':
    app.run(debug=True)