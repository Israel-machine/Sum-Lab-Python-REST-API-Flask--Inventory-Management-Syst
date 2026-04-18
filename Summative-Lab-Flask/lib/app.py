from flask import Flask, request, jsonify
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.data import products
from utils.io_file import save_data, load_data
import random

#----APP INIT----
app = Flask(__name__)

load_data()
#Event Class:
class Product:
    def __init__(self, name, brands, price):
        self.code = ''.join([str(random.randint(0, 9)) for _ in range(14)])
        self.name = name
        self.brands = brands
        self.price = price

    def to_dict(self): #convert to dictionary for json use
        return {
            "code": self.code,
            "product": {"id": self.code},
            "name": self.name,
            "brands": self.brands,
            "price": self.price
        }

def fetch_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product = data["product"]
                return {
                    "name": product.get("product_name", "Unknown"),
                    "brands": product.get("brands", "Unknown")
                }
    except Exception as e:
        print(f"External API Error: {e}")
    return None

@app.route("/inventory/fetch/<barcode>", methods=["POST"])
def fetch_and_add_product(barcode):
    if any(p["code"] == barcode for p in products):
        return jsonify({"error": "Product already in inventory"}), 400

    external_data = fetch_from_openfoodfacts(barcode)
    
    if external_data:
        new_product = {
            "code": barcode,
            "product": {"id": barcode},
            "name": external_data["name"],
            "brands": external_data["brands"],
            "price": 0.0  # Set a default price
        }
        products.append(new_product)
        save_data()
        return jsonify(new_product), 201
    
    return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

#---RESTFUL ROUTES----:
# GET /inventory → Fetch all items
@app.route("/inventory", methods=["GET"])
def get_products():#take all products in products list and turn into dict. versio of themselves
    return jsonify(products), 200

# GET /inventory/<id> → Fetch a single item
@app.route("/inventory/<id>", methods=["GET"])
def get_event(id):
    product = next((p for p in products if p["product"]["id"] == id ), None) #WHAT IS THIS?
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

# POST /inventory → Add a new item
@app.route("/inventory", methods=["POST"])
def create_event():
    data = request.get_json() #will grab body of data
    new_obj = Product(name=data["name"], brands=data["brands"], price=data["price"])
    new_product_dict = new_obj.to_dict()
    products.append(new_product_dict) 
    save_data()
    return jsonify(new_product_dict), 201

# PATCH /inventory/<id> → Update an item
@app.route("/inventory/<id>", methods=["PATCH"])
def update_product(id):#uses id from URL parameter
    data = request.get_json() #grab data that user sent, will manipulate "title"
    product = next((p for p in products if p["product"]["id"] == id), None) #grab event using id passed in
    if not product: #checks if event exists
        return jsonify({"error": "Product not found"}), 404
    if "name" in data:
        product["name"] = data["name"]
        save_data()
    if "price" in data:
        product["price"] = data["price"]
        save_data()
    return jsonify(product), 200

# DELETE /inventory/<id> → Remove an item
@app.route("/inventory/<id>", methods=["DELETE"])
def delete_product(id):
    product = next((p for p in products if p["product"]["id"] == id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    products[:] = [p for p in products if p["product"]["id"] != id]
    save_data()
    return "", 204


#APP RUNS WHEN FILE RUNS
if __name__ == "__main__":
    app.run(debug=True)