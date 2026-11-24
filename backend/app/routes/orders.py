import uuid
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from pymongo import ReturnDocument
from ..utils import admin_required, current_user_id, get_id, serialize, now
bp = Blueprint("orders", __name__)
VALID_STATUSES = {"Processing", "Packed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"}

@bp.post("/orders")
@jwt_required()
def checkout():
    data = request.get_json(silent=True) or {}; address = data.get("shippingAddress", {}); payment = data.get("paymentMethod", "COD")
    required = ("fullName", "line1", "city", "postalCode", "phone")
    if not all(str(address.get(x, "")).strip() for x in required) or payment not in {"COD", "RAZORPAY"}: return jsonify({"message": "Complete shipping address and valid payment method required"}), 400
    cart = current_app.db.carts.find_one({"userId": current_user_id()})
    if not cart or not cart["items"]: return jsonify({"message": "Cart is empty"}), 400
    items = []
    for line in cart["items"]:
        product = current_app.db.products.find_one_and_update({"_id": line["productId"], "stock": {"$gte": line["quantity"]}}, {"$inc": {"stock": -line["quantity"]}}, return_document=ReturnDocument.AFTER)
        if not product:
            for done in items: current_app.db.products.update_one({"_id": done["productId"]}, {"$inc": {"stock": done["quantity"]}})
            return jsonify({"message": f"{line['name']} is no longer in stock"}), 409
        items.append({**line, "productId": product["_id"]})
    subtotal = round(sum(x["price"] * x["quantity"] for x in items), 2); shipping = 0 if subtotal >= 499 else 49
    order = {"orderNumber": f"SS-{uuid.uuid4().hex[:8].upper()}", "userId": current_user_id(), "items": items, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping, "shippingAddress": address, "paymentMethod": payment, "paymentStatus": "Pending", "status": "Processing", "createdAt": now(), "updatedAt": now()}
    current_app.db.orders.insert_one(order); current_app.db.carts.update_one({"_id": cart["_id"]}, {"$set": {"items": []}})
    return jsonify({"order": serialize(order)}), 201

@bp.get("/orders")
@jwt_required()
def orders(): return jsonify({"orders": serialize(list(current_app.db.orders.find({"userId": current_user_id()}).sort("createdAt", -1)))})

@bp.get("/orders/<order_id>")
@jwt_required()
def order(order_id):
    item = current_app.db.orders.find_one({"_id": get_id(order_id), "userId": current_user_id()})
    return (jsonify({"order": serialize(item)}), 200) if item else (jsonify({"message": "Order not found"}), 404)

@bp.get("/admin/orders")
@admin_required
def admin_orders(): return jsonify({"orders": serialize(list(current_app.db.orders.find().sort("createdAt", -1)))})

@bp.patch("/admin/orders/<order_id>")
@admin_required
def update_order(order_id):
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in VALID_STATUSES: return jsonify({"message": "Invalid status"}), 400
    result = current_app.db.orders.update_one({"_id": get_id(order_id)}, {"$set": {"status": status, "updatedAt": now()}})
    return (jsonify({"message": "Order updated"}), 200) if result.matched_count else (jsonify({"message": "Order not found"}), 404)
