from flask import Blueprint, current_app, jsonify
from ..utils import admin_required, current_user_id, serialize
from flask_jwt_extended import jwt_required
bp = Blueprint("dashboard", __name__)
@bp.get("/dashboard/customer")
@jwt_required()
def customer():
    orders = list(current_app.db.orders.find({"userId": current_user_id()}).sort("createdAt", -1).limit(5))
    return jsonify({"recentOrders": serialize(orders), "orderCount": current_app.db.orders.count_documents({"userId": current_user_id()})})
@bp.get("/dashboard/admin")
@admin_required
def admin():
    db = current_app.db; orders = list(db.orders.find({"status": {"$ne": "Cancelled"}}))
    return jsonify({"sales": sum(x["total"] for x in orders), "orders": db.orders.count_documents({}), "customers": db.users.count_documents({"role": "user"}), "inventory": sum(x.get("stock", 0) for x in db.products.find())})
