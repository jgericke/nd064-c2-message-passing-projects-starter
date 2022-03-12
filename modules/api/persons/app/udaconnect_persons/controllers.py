from datetime import datetime

from app.udaconnect_persons.models import Person
from app.udaconnect_persons.schemas import (
    PersonSchema,
)
from app.udaconnect_persons.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields
from typing import Optional, List


api = Namespace("UdaConnect Persons", description="UdaConnect Persons API.")  # noqa
post_model = api.model(
    "Person",
    {
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "company_name": fields.String(required=True, description="Company name"),
    },
)

# TODO: This needs better exception handling


@api.route("/persons")
class PersonsResource(Resource):
    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons

    @api.expect(post_model)
    @api.marshal_with(post_model, code=201)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        new_person: Person = PersonService.create(request.get_json())
        return new_person


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
