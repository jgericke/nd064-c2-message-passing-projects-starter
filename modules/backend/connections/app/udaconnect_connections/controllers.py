from app.udaconnect_connections.models import Connection
from app.udaconnect_connections.schemas import (
    ConnectionSchema,
)
from app.udaconnect_connections.services import (
    ConnectionService,
)
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List


api = Namespace(
    "UdaConnect Connections", description="UdaConnect Connections Mapping API"
)


@api.route("/connections/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
