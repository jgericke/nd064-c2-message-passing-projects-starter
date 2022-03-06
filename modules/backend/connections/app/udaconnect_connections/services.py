import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db, config
from app.udaconnect_connections.models import Connection, Location, Person
from app.udaconnect_connections.schemas import PersonSchema

from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

import grpc
from protos import location_pb2
from protos import location_pb2_grpc

import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("connections-api")

DATE_FORMAT = "%Y-%m-%d"

# Initialize GPRC channel
grpc_channel = grpc.insecure_channel(config.GRPC_URI)

# Set persons REST API endpoint
persons_api = f"{config.PERSONS_URI}/api/persons"


class ConnectionService:
    @staticmethod
    def find_contacts(
        person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:

        # Retrieve location range for person_id via GRPC channel
        locations_stub = location_pb2_grpc.LocationServiceStub(grpc_channel)
        locations_resp = locations_stub.GetLocationRange(
            location_pb2.GetLocationRangeRequest(
                person_id=int(person_id), start_date=start_date, end_date=end_date
            )
        )
        # Convert locations_resp.locations
        locations: List = locations_resp.locations

        # Retrieve persons from person service API
        persons_resp = requests.get(persons_api)
        persons_resp.raise_for_status()
        persons = persons_resp.json()

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person["id"]: person for person in persons}

        # Prepare arguments for queries - Note date reformating for delta
        data = []
        for location in locations:

            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date,
                    "end_date": (
                        datetime.strptime(end_date, DATE_FORMAT) + timedelta(days=1)
                    ).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id],
                        location=location,
                    )
                )

        return result


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
