from flask import Flask, request, jsonify
from data import products  # Import from the neutral data file
import random


#----APP INIT----
app = Flask(__name__)

#Event Class:
class Product:
# Generates a 14-digit integer and converts to string
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
        return ({"Product now found"}), 404

# POST /inventory → Add a new item
@app.route("/inventory", methods=["POST"])
def create_event():
    data = request.get_json() #will grab body of data
    new_obj = Product(name=data["name"], brands=data["brands"], price=data["price"])
    new_product_dict = new_obj.to_dict()
    products.append(new_product_dict) 
    
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
    if "price" in data:
        product["price"] = data["price"]
    return jsonify(product), 200

# DELETE /inventory/<id> → Remove an item
@app.route("/inventory/<id>", methods=["DELETE"])
def delete_product(id):
    product = next((p for p in products if p["product"]["id"] == id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    products[:] = [p for p in products if p["product"]["id"] != id]
    return "", 204


#APP RUNS WHEN FILE RUNS
if __name__ == "__main__":
    app.run(debug=True)