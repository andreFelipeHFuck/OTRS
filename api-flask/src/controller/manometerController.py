from flask import request, make_response, jsonify
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError


from src.config.dbConnect import InfluxClient, bucket, org
from src.models.manometer import Manometer

class ManometerController:
    @staticmethod
    def _createManometerToJson(req):
        manometer = Manometer(
            manometer_id=req['manometer_id'],
            measurement_name=req['measurement_name'],
            location=req['location']
        )
        return manometer

    @staticmethod
    def createManometerPoint(req):
        manometer = ManometerController._createManometerToJson(req=req)
        point = manometer.create_point(state=True, value=0.1)
        print(point)

        try:
            write_api = InfluxClient.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=point)
            return make_response(
                 jsonify({'message': "File sent successfully", 'point': f"{point}"}),
                  200
                )
        except InfluxDBError as e:
            raise e
            return make_response(
               jsonify({"error": "No files found, file not in request"}),
                400
            )