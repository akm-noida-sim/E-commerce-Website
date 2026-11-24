from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils import admin_required, get_id, serialize, now
bp = Blueprint("products", __name__)
FIELDS = ("name", "description", "price", "category", "image", "stock")

@bp.get("/products")
def list_products():
    q = request.args.get("q", "").strip(); category = request.args.get("category")
    query = {"name": {"$regex": q, "$options": "i"}} if q else {}
    if category: query["category"] = category
    sort = {"price_asc": ("price", 1), "price_desc": ("price", -1), "newest": ("createdAt", -1)}.get(request.args.get("sort"), ("createdAt", -1))
    products = list(current_app.db.products.find(query).sort(*sort))
    return jsonify({"products": serialize(products), "count": len(products)})

@bp.get("/products/<product_id>")
def product(product_id):
    item = current_app.db.products.find_one({"_id": get_id(product_id)})
    return (jsonify({"product": serialize(item)}), 200) if item else (jsonify({"message": "Product not found"}), 404)

@bp.post("/products")
@admin_required
def create_product():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("category") or float(data.get("price", -1)) < 0 or int(data.get("stock", -1)) < 0: return jsonify({"message": "Name, category, valid price and stock are required"}), 400
    product = {key: data.get(key) for key in FIELDS}; product.update({"price": float(product["price"]), "stock": int(product["stock"]), "createdAt": now()})
    current_app.db.products.insert_one(product)
    return jsonify({"product": serialize(product)}), 201

@bp.route("/products/<product_id>", methods=["PUT", "DELETE"])
@admin_required
def modify_product(product_id):
    _id = get_id(product_id)
    if request.method == "DELETE":
        result = current_app.db.products.delete_one({"_id": _id}); return ("", 204) if result.deleted_count else (jsonify({"message": "Product not found"}), 404)
    data = {k:v for k,v in (request.get_json(silent=True) or {}).items() if k in FIELDS}
    if "price" in data: data["price"] = float(data["price"])
    if "stock" in data: data["stock"] = int(data["stock"])
    current_app.db.products.update_one({"_id": _id}, {"$set": data})
    item = current_app.db.products.find_one({"_id": _id}); return (jsonify({"product": serialize(item)}), 200) if item else (jsonify({"message": "Product not found"}), 404)

@bp.get("/categories")
def categories(): return jsonify({"categories": current_app.db.products.distinct("category")})
