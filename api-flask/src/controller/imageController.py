import datetime

from flask import request, make_response, jsonify

import base64
import os

from helpers import allowed_file, UPLOAD_FOLDER

class ImageController:
    @staticmethod
    def uploadImage(image_data, foldername:str):
        try:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            else:
                if not os.path.exists(f"{UPLOAD_FOLDER}/{foldername}"):
                    os.makedirs(f"{UPLOAD_FOLDER}/{foldername}")

            image_bytes = base64.b64decode(image_data)

            timestamp = datetime.datetime.now()
            file_path = os.path.join(
                    UPLOAD_FOLDER, 
                    f"{foldername}/{foldername}-{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                )

            with open(file_path, "wb") as f:
                f.write(image_bytes)

            return file_path
        
        except Exception as e:
            raise e

    @staticmethod
    def processImage(image_path:str):
        return True, 0.1

    @staticmethod
    def deleteImage(image_path:str):
        try:
            os.remove(image_path)
        except Exception as e:
            raise e


