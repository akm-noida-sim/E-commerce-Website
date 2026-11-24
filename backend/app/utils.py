from bson import ObjectId
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc)
def serialize(value):
    if isinstance(value, ObjectId): return str(value)
    if isinstance(value, datetime): return value.isoformat()
    if isinstance(value, list): return [serialize(x) for x in value]
    if isinstance(value, dict): return {k: serialize(v) for k,v in value.items()}
    return value

def get_id(value):
    try: return ObjectId(value)
    except Exception: return None

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt().get("role") != "admin": return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def current_user_id(): return get_id(get_jwt_identity())
