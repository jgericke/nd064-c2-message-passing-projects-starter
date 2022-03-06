from app.udaconnect_persons.models import Person  # noqa
from app.udaconnect_persons.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect_persons.controllers import api as udaconnect_persons_api

    api.add_namespace(udaconnect_persons_api, path=f"/{root}")
