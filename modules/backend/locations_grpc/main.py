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
        logger.info("received request for locations")
        # Retrieve all locations
        locations: List[Location] = LocationService.retrieve_all()

        # Marshal location to Location protobuf
        location_list = []
        for location in LocationSchema(many=True).dump(locations):
            location_message = location_pb2.Location()
            location_list.append(json_format.ParseDict(location, location_message))

        result = location_pb2.LocationList()
        result.locations.extend(location_list)
        return result

    def GetLocation(self, request, context):
        logger.info("received request for location id: {}".format(request.id))
        location: Location = LocationService.retrieve(request.id)

        result = location_pb2.Location()
        return json_format.ParseDict(LocationSchema().dump(location), result)

    def Create(self, request, context):

        logger.info("received location creation request")

        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }

        location: Location = LocationService.create(request_value)
        result = location_pb2.Location()
        return json_format.ParseDict(LocationSchema().dump(location), result)


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
