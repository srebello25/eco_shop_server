# Sibelius_Rebello_HE29743_SWE4303

#import the flask modules which are needed
from flask import Flask, jsonify, request

# Import functions which are related to JWT
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

# To set expiration of Token import timedelta
from datetime import timedelta

# Creating an application instance of Flask
app = Flask(__name__)

##-- Configuration of JWT

# Replace with strong secret key used for encoding JWT token in production
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Setting access token validation(how long- set to 45 days)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=45)

# Initialization of JWT manager with Flask app
jwt = JWTManager(app)

##-- Mock user data and shared cart

# username and passwords which are simulated this would normally be in a database
users = {
    "user@123": "password@@",
    "admin@456": "@@password"
}
# Dictionary to hold shopping carts which are specific to user
user_carts = {}

##--Routes

# Testing the home route to confirm API is working
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Eco-Friendly E-Commerce!"})

# ping route to check connectivity
@app.route('/api/ping')
def ping():
    return jsonify({
        "response": "pong",
        # server name and port name shown ( helpful in load balancing)
        "served_by": request.environ.get('SERVER_NAME', 'unknown') + ':' +
                     request.environ.get('SERVER_PORT', 'unknown')
    })

# route to return the lists of products
@app.route('/api/products')
def get_products():
    products = [
        {"id": 1, "name": "Eco Bamboo Toothbrush", "price": 4.99},
        {"id": 2, "name": "Paper Bags Reusable", "price": 5.99},
        {"id": 3, "name": "Biodegradable Cups Pack", "price": 7.99}
    ]
    return jsonify({"products": products})

# route used to login , authenticate users and return a JWT token
@app.route('/api/login', methods=['POST'])
def login():
    # input from the request (JSON Parsing)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Checking if the user exists and matches the password
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# route which is protected for the product to be added to the user's cart
@app.route('/api/cart/add', methods=['POST'])
@jwt_required() #Valid JWT token required
def add_to_cart():
    # Getting the current user's identity from the JWT token
    current_user = get_jwt_identity()
    #  input to get product details(JSON Parsing)
    data = request.get_json()
    product = data.get('product')

    # input Validation
    if not product:
        return jsonify({"msg": "No product provided"}), 400

    # Initializing the user's cart if it is not existing
    if current_user not in user_carts:
        user_carts[current_user] = []

    # Adding product to the user's cart
    user_carts[current_user].append(product)
    return jsonify({"msg": "Product added", "cart": user_carts[current_user]}), 200

# Protected route to view the user's current cart
@app.route('/api/cart/view', methods=['GET'])
@jwt_required() #Requires Valid JWT token
def view_cart():
    # Getting the current user's identity from the JWT token
    current_user = get_jwt_identity()

    # User's cart is retrieved or an empty list returned
    cart = user_carts.get(current_user, [])
    return jsonify({"cart": cart}), 200

##--Serving static file

from flask import send_from_directory
# Static files serving route (e.g. index.html, CSS, JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# #--Run app locally in debug mode for development and testing purpose only
# #Not for production use. Use WSGI server like Gunicorn instead
# # Uncomment the below lines to run locally
# if __name__ == '__main__':
#    #  Start flask in debug mode (use this only in development!)
#    app.run(debug=True)




