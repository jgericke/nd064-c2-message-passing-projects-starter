def register_routes(api, app, root="api"):
    from app.udaconnect_locations import register_routes as attach_udaconnect_locations

    # Add routes
    attach_udaconnect_locations(api, app)
