from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils import current_user_id, get_id, serialize, now
bp = Blueprint("cart", __name__)
def cart_for_user(): return current_app.db.carts.find_one({"userId": current_user_id()})
def output(cart): return {"cart": serialize(cart or {"items": []})}

@bp.get("/cart")
@jwt_required()
def get_cart(): return jsonify(output(cart_for_user()))

@bp.post("/cart/items")
@jwt_required()
def add_item():
    data = request.get_json(silent=True) or {}; product = current_app.db.products.find_one({"_id": get_id(data.get("productId"))})
    quantity = int(data.get("quantity", 1))
    if not product or quantity < 1: return jsonify({"message": "Valid product and quantity are required"}), 400
    if product["stock"] < quantity: return jsonify({"message": "Insufficient stock"}), 409
    cart = cart_for_user(); items = cart["items"] if cart else []
    found = next((x for x in items if x["productId"] == product["_id"]), None)
    if found:
        if found["quantity"] + quantity > product["stock"]: return jsonify({"message": "Insufficient stock"}), 409
        found["quantity"] += quantity
    else: items.append({"productId": product["_id"], "name": product["name"], "price": product["price"], "image": product.get("image", ""), "quantity": quantity})
    current_app.db.carts.update_one({"userId": current_user_id()}, {"$set": {"items": items, "updatedAt": now()}}, upsert=True)
    return jsonify(output(cart_for_user())), 201

@bp.patch("/cart/items/<product_id>")
@jwt_required()
def update_item(product_id):
    quantity = int((request.get_json(silent=True) or {}).get("quantity", 0)); cart = cart_for_user()
    if not cart: return jsonify({"message": "Cart not found"}), 404
    product_id = get_id(product_id); items = cart["items"]
    item = next((x for x in items if x["productId"] == product_id), None)
    if not item: return jsonify({"message": "Cart item not found"}), 404
    if quantity <= 0: items.remove(item)
    else:
        product = current_app.db.products.find_one({"_id": product_id})
        if not product or quantity > product["stock"]: return jsonify({"message": "Insufficient stock"}), 409
        item["quantity"] = quantity
    current_app.db.carts.update_one({"_id": cart["_id"]}, {"$set": {"items": items, "updatedAt": now()}})
    return jsonify(output(cart_for_user()))
