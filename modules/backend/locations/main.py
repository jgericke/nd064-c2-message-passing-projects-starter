import logging
import json
import time
from datetime import datetime

from udaconnect_locations.models import Location
from udaconnect_locations.schemas import (
    LocationSchema,
)
from udaconnect_locations.services import LocationService
from typing import Optional, List

from concurrent import futures
import grpc
from protos import location_pb2
from protos import location_pb2_grpc

from google.protobuf import json_format

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locations")

DATE_FORMAT = "%Y-%m-%d"


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        logger.info("Received request for locations")
        # Retrieves list of all locations
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
        logger.info(f"Received request for location id: {request.id}")
        # Retrieves single location
        location: Location = LocationService.retrieve(location_id=request.id)

        result = location_pb2.Location()
        return json_format.ParseDict(LocationSchema().dump(location), result)

    def GetLocationRange(self, request, context):

        # Parse location range request
        lr_request = {
            "person_id": request.person_id,
            "start_date": request.start_date,
            "end_date": request.end_date,
        }

        logger.info(f"Received request for location range: {lr_request}")

        start_date: datetime = datetime.strptime(lr_request["start_date"], DATE_FORMAT)
        end_date: datetime = datetime.strptime(lr_request["end_date"], DATE_FORMAT)

        # Retrieve list of locations for person_id based on start and end_dates
        locations: List[Location] = LocationService.retrieve_range(
            person_id=lr_request["person_id"], start_date=start_date, end_date=end_date
        )
        logger.info(f"location range {locations}")

        # Marshal location range result to Location protobuf
        location_range_list = []
        for location in LocationSchema(many=True).dump(locations):
            location_message = location_pb2.Location()
            location_range_list.append(
                json_format.ParseDict(location, location_message)
            )

        result = location_pb2.LocationList()
        result.locations.extend(location_range_list)
        return result

    def Create(self, request, context):

        # Parse location range request
        l_request = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }

        logger.info(f"Received location creation request: {l_request}")

        location: Location = LocationService.create(l_request)

        result = location_pb2.Location()
        return json_format.ParseDict(LocationSchema().dump(location), result)


if __name__ == "__main__":

    logger.info("Starting LocationService (max_woerks=2) on port: 5005")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

    server.add_insecure_port("[::]:5005")
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
