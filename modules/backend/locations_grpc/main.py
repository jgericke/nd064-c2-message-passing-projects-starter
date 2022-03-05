import logging
import json
import time
from datetime import datetime

from models import Location
from schemas import (
    LocationSchema,
)
from services import LocationService
from typing import Optional, List

from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc


from google.protobuf import json_format

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locations")


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):

        locations: List[Location] = LocationService.retrieve_all()

        location_message_list = []
        for location in LocationSchema(many=True).dump(locations):
            location_message = location_pb2.LocationMessage()
            location_message_list.append(
                json_format.ParseDict(location, location_message)
            )

        locations_str = {
            "id": 1,
            "person_id": 5,
            "longitude": "37.4363",
            "latitude": "-122.290843",
            "creation_time": "2021-07-07T10:37:06",
        }

        print(type(location_message_list[0]))

        # logger.info(type(json.dumps(LocationSchema(many=True).dump(locations))))
        result = location_pb2.LocationMessageList()
        result.locations.extend(location_message_list)
        return result

    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }
        print(request_value)

        return location_pb2.LocationMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
