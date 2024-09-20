from datetime import datetime
import os

from flask import request, jsonify, make_response
from flask_restful import Resource

from src.controller.manometerController import ManometerController
from src.controller.imageController import ImageController

class ManometerRouters(Resource):
    def get(self):
        pass
    
    def post(self):
        try:
            res_json = request.json

            image_path= ImageController.uploadImage(image_data=res_json['value'], foldername=res_json['manometer_id'])
            state, value = ImageController.processImage(image_path=image_path)
            ManometerController.createManometerPoint(req=res_json, state=state, value=value)

            return make_response(
                    jsonify({
                        'message': "File sent successfully",
                        }),
                    200
                )
        
        except Exception as e:
            ImageController.deleteImage(image_path=image_path)
            return make_response(
                jsonify({"error": f"{e}"}),
                400
            )

class ManometersRouters(Resource):
    ...
