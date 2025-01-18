from flask import Flask, request, make_response, jsonify
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(include_pizzas=False) for restaurant in restaurants])

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict())  # restaurant_pizzas included by default

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.query(RestaurantPizza).filter(RestaurantPizza.restaurant_id == id).delete()
    db.session.delete(restaurant)
    db.session.commit()
    
    return '', 204

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(include_restaurant=False) for pizza in pizzas])

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")
    price = data.get("price")

    # Validation: Check if the price is between 1 and 30
    if not (1 <= price <= 30):
        return jsonify({"errors": ["validation errors"]}), 400
    
    # Check if the pizza and restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza:
        return jsonify({"errors": ["Pizza not found"]}), 404
    if not restaurant:
        return jsonify({"errors": ["Restaurant not found"]}), 404

    # Create a new RestaurantPizza object
    restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id,
        restaurant_id=restaurant_id,
        price=price
    )

    # Add to the database and commit the changes
    db.session.add(restaurant_pizza)
    db.session.commit()

    # Return a success response with a 201 Created status code
    return jsonify(restaurant_pizza.to_dict()), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
