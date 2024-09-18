from datetime import datetime
import os

from flask import request, jsonify, make_response
from flask_restful import Resource, fields

from helpers import allowed_file, UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

data = [
    {
        "manometer_id": 1,
        "time_series": [
            (datetime(2020, 5, 7), "URL1", True),
            (datetime(2020, 5, 7), "URL2", True),
            (datetime(2020, 5, 7), "URL3", True),
            (datetime(2020, 5, 7), "URL4", False)
        ]
    },
    {
        "manometer_id": 2,
        "time_series": [
            (datetime(2020, 5, 7), "URL1", True),
            (datetime(2020, 5, 7), "URL2", True),
            (datetime(2020, 5, 7), "URL3", True),
            (datetime(2020, 5, 7), "URL4", False)
        ]
    }
]

state_fields = {
    'datetime': fields.DateTime,
    'image_url': fields.Url,
    'level': fields.Boolean
}

resource_fields = {
    'manometer_id': fields.Integer,
    'time_series': fields.List(
        fields.List(fields.Nested(state_fields))
    )
}

class ManometerRouters(Resource):
    def get(self, manometer_id:int):
        return jsonify(data)
    
    def post(self):
        if 'file' not in request.files:
            return make_response(
                jsonify({"error": "No files found, file not in request"}),
                400
            )
        
        file = request.files['file']

        if file.filename == '':
            return make_response(
                jsonify({"error": "No files found, filename is empty"}),
                400
            )
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            with open(file_path, "wb") as f:
                file.save(file_path)

            return make_response(
                jsonify({'message': f"File {filename} sent successfully", 'file_path': file_path}),
                200
            )

        return make_response(
                jsonify({"error": "No files found"}),
                400
            )
        
    
class ManometersRouters(Resource):
    ...
