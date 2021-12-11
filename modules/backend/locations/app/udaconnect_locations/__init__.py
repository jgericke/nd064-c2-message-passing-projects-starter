from app.udaconnect_locations.models import Location, Person  # noqa
from app.udaconnect_locations.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udaconnect_locations.controllers import api as udaconnect_locations_api

    api.add_namespace(udaconnect_locations_api, path=f"/{root}")
