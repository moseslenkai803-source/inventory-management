from flask import Flask, jsonify, request, render_template

from inventory import inventory
import inventory as inventory_data
from openfoodfacts_service import (
    OpenFoodFactsError,
    fetch_product_by_barcode,
    search_products_by_name,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404



@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    new_item = request.get_json(silent=True)

    if not isinstance(new_item, dict):
        return jsonify({"error": "Invalid input"}), 400

    if "id" in new_item:
        return jsonify({"error": "Do not provide an ID"}), 400

    required_fields = ["name", "category", "quantity", "price"]

    for field in required_fields:
        if field not in new_item:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if (
        not isinstance(new_item["quantity"], int)
        or isinstance(new_item["quantity"], bool)
        or new_item["quantity"] < 0
    ):
        return jsonify({"error": "Quantity must be non-negative"}), 400

    if (
        not isinstance(new_item["price"], (int, float))
        or isinstance(new_item["price"], bool)
        or new_item["price"] < 0
    ):
        return jsonify({"error": "Price must be non-negative"}), 400

    new_item["id"] = inventory_data.next_id
    inventory.append(new_item)
    inventory_data.next_id += 1

    return jsonify(new_item), 201



@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    allowed_fields = {
        "name",
        "barcode",
        "category",
        "quantity",
        "price",
        "brand",
        "ingredients",
        "image_url",
        "source",
    }

    update_data = request.get_json(silent=True)

    if not isinstance(update_data, dict):
        return jsonify({"error": "Invalid input"}), 400



    if not update_data.keys() <= allowed_fields:
        return jsonify({"error": "Unknown field"}), 400

    if "quantity" in update_data:
        quantity = update_data["quantity"]

        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity < 0
        ):
            return jsonify({"error": "Quantity must be non-negative"}), 400

    if "price" in update_data:
        price = update_data["price"]

        if (
            not isinstance(price, (int, float))
            or isinstance(price, bool)
            or price < 0
        ):
            return jsonify({"error": "Price must be non-negative"}), 400

    for key, value in update_data.items():
        item[key] = value

    return jsonify(item), 200



@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200


@app.route("/products/barcode/<barcode>", methods=["GET"])
def get_product_by_barcode(barcode):
    try:
        product = fetch_product_by_barcode(barcode)
    except OpenFoodFactsError as exc:
        return jsonify({"error": str(exc)}), 502

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.route("/products/search", methods=["GET"])
def search_products():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({"error": "Query parameter 'name' is required"}), 400

    try:
        products = search_products_by_name(name)
    except OpenFoodFactsError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(products), 200

if __name__ == "__main__":
    app.run(debug=True)
