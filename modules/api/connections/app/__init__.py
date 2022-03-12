from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# GRPC required for locations range retrieval
import grpc

# Kafka required for emitting connection results
from kafka import KafkaProducer

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect Connections API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.before_request
    def before_request():
        # Initialize GPRC channel
        g.grpc_channel = grpc.insecure_channel(app.config["LOCATIONS_GRPC_URI"])

        # Set up a Kafka producer
        g.kafka_producer = KafkaProducer(bootstrap_servers=app.config["KAFKA_URI"])

    return app
