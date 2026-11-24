import bcrypt
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from ..utils import serialize, current_user_id, now

bp = Blueprint("auth", __name__)
def public_user(user): return {"id": str(user["_id"]), "name": user["name"], "email": user["email"], "role": user["role"]}
def token(user): return create_access_token(identity=str(user["_id"]), additional_claims={"role": user["role"]})

@bp.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    name, email, password = data.get("name", "").strip(), data.get("email", "").strip().lower(), data.get("password", "")
    if len(name) < 2 or "@" not in email or len(password) < 8: return jsonify({"message": "Name, valid email, and an 8-character password are required"}), 400
    users = current_app.db.users
    if users.find_one({"email": email}): return jsonify({"message": "Email is already registered"}), 409
    user = {"name": name, "email": email, "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), "role": "user", "createdAt": now()}
    users.insert_one(user)
    return jsonify({"token": token(user), "user": public_user(user)}), 201

@bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}; user = current_app.db.users.find_one({"email": data.get("email", "").lower()})
    if not user or not bcrypt.checkpw(data.get("password", "").encode(), user["password"].encode()): return jsonify({"message": "Invalid email or password"}), 401
    return jsonify({"token": token(user), "user": public_user(user)})

@bp.get("/auth/me")
@jwt_required()
def me():
    user = current_app.db.users.find_one({"_id": current_user_id()}, {"password": 0})
    return jsonify({"user": serialize(user)}) if user else (jsonify({"message": "User not found"}), 404)
