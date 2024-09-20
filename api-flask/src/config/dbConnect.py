from datetime import datetime
from dotenv import load_dotenv, main
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

token = os.getenv('INFLUXDB_TOKEN')
org = os.getenv('ORG')
bucket = os.getenv('BUCKET')

InfluxClient = InfluxDBClient(url="http://localhost:8086", token=token)

# READ QUERY

# query_api = InfluxClient.query_api()

# query = """from(bucket: "Manometros")
#  |> range(start: -10m)
#  |> filter(fn: (r) => r._measurement == "measurement1")"""
# tables = query_api.query(query, org="UDESC")

# for table in tables:
#   for record in table.records:
#     print(record)

# OTHER QUERY

# query_api = write_client.query_api()

# query = """from(bucket: "Manometros")
#   |> range(start: -10m)
#   |> filter(fn: (r) => r._measurement == "measurement1")
#   |> mean()"""
# tables = query_api.query(query, org="UDESC")

# for table in tables:
#     for record in table.records:
#         print(record)
