def register_routes(api, app, root="api"):
    from app.udaconnect_connections.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
