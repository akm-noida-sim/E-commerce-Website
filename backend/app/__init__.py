import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv

mongo = None

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt-change-me"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=int(os.getenv("ACCESS_TOKEN_EXPIRES_HOURS", "24"))),
        MONGO_URI=os.getenv("MONGO_URI", "mongodb://localhost:27017/shopsphere"),
    )
    if test_config:
        app.config.update(test_config)
    CORS(app, resources={r"/api/*": {"origins": os.getenv("CLIENT_ORIGIN", "http://localhost:5173")}})
    JWTManager(app)
    global mongo
    mongo = app.config.get("MONGO_CLIENT")
    if mongo is None:
        mongo = MongoClient(app.config["MONGO_URI"])
    app.db = mongo.get_database() if not app.config.get("MONGO_DB") else app.config["MONGO_DB"]
    from .routes import auth, products, cart, orders, dashboard
    for blueprint in (auth.bp, products.bp, cart.bp, orders.bp, dashboard.bp):
        app.register_blueprint(blueprint, url_prefix="/api")
    @app.get("/api/health")
    def health(): return jsonify({"status": "ok"})
    @app.errorhandler(404)
    def not_found(_): return jsonify({"message": "Resource not found"}), 404
    return app
