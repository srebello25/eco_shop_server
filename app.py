from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

app = Flask(__name__)

# ----------------------------
# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Use a strong key in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=45)  # Token expires after 45 days
jwt = JWTManager(app)

# ----------------------------
# Home and Ping Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Eco-Friendly E-Commerce!"})

@app.route('/api/ping')
def ping():
    return jsonify({
        "response": "pong",
        "served_by": request.environ.get('SERVER_NAME', 'unknown') + ':' +
                     request.environ.get('SERVER_PORT', 'unknown')
    })

# ----------------------------
# Product Listings
@app.route('/api/products')
def get_products():
    products = [
        {"id": 1, "name": "Eco Bamboo Toothbrush", "price": 3.99},
        {"id": 2, "name": "Reusable Cotton Bags", "price": 5.49},
        {"id": 3, "name": "Biodegradable Plates Pack", "price": 9.99}
    ]
    return jsonify({"products": products})

# ----------------------------
# Mock user credentials
users = {
    "user1": "password123",
    "admin": "adminpass"
}

# Shared carts per JWT identity
user_carts = {}

# ----------------------------
# Login Route (returns JWT)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# ----------------------------
# Add Product to Cart (JWT protected)
@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    data = request.get_json()
    product = data.get('product')

    if not product:
        return jsonify({"msg": "No product provided"}), 400

    if current_user not in user_carts:
        user_carts[current_user] = []

    user_carts[current_user].append(product)
    return jsonify({"msg": "Product added", "cart": user_carts[current_user]}), 200

# ----------------------------
# View Cart (JWT protected)
@app.route('/api/cart/view', methods=['GET'])
@jwt_required()
def view_cart():
    current_user = get_jwt_identity()
    cart = user_carts.get(current_user, [])
    return jsonify({"cart": cart}), 200

# ----------------------------
# Run Flask (for development testing)
if __name__ == '__main__':
    app.run(debug=True)



# ----------------------------
# Product Listings
@app.route('/api/products')
def get_products():
    products = [
        {"id": 1, "name": "Eco Bamboo Toothbrush", "price": 3.99},
        {"id": 2, "name": "Reusable Cotton Bags", "price": 5.49},
        {"id": 3, "name": "Biodegradable Plates Pack", "price": 9.99}
    ]
    return jsonify({"products": products})

# ----------------------------
# Mock user credentials
users = {
    "user1": "password123",
    "admin": "adminpass"
}

# Shared carts per JWT identity
user_carts = {}

# ----------------------------
# Login Route (returns JWT)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# ----------------------------
# Add Product to Cart (JWT protected)
@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    current_user = get_jwt_identity()
    data = request.get_json()
    product = data.get('product')

    if not product:
        return jsonify({"msg": "No product provided"}), 400

    if current_user not in user_carts:
        user_carts[current_user] = []

    user_carts[current_user].append(product)
    return jsonify({"msg": "Product added", "cart": user_carts[current_user]}), 200

# ----------------------------
# View Cart (JWT protected)
@app.route('/api/cart/view', methods=['GET'])
@jwt_required()
def view_cart():
    current_user = get_jwt_identity()
    cart = user_carts.get(current_user, [])
    return jsonify({"cart": cart}), 200

# ----------------------------
# Run Flask (for development testing)
if __name__ == '__main__':
    app.run(debug=True)

