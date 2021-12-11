def register_routes(api, app, root="api"):
    from app.udaconnect_persons import register_routes as attach_udaconnect_persons

    # Add routes
    attach_udaconnect_persons(api, app)
