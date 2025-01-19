# Flask Restaurant Pizza API
This repository contains a Flask application that uses SQLAlchemy to manage data for restaurants, pizzas, and their relationships. The application allows you to manage restaurants, pizzas, and the prices of pizzas offered by restaurants.

The models defined in the application represent the following entities:

1.Restaurant
2.Pizza
3.RestaurantPizza (The association model between restaurants and pizzas, with additional information like price)
## Table of Contents
Installation

Models

  Restaurant Model

  Pizza Model

  RestaurantPizza Model

Relationships

Custom Methods

SerializerMixin

Example Usage

Running the Application

Contributing

License

## Installation
To run the Flask application with SQLAlchemy, you’ll need to have the following dependencies installed:

1.Flask

2.Flask-SQLAlchemy

3.SQLAlchemy

4.sqlalchemy-serializer

## Steps to Install
1.Clone the repository:
```
git clone <repository_url>
```
2.Install the required dependencies:
```
pip install Flask Flask-SQLAlchemy SQLAlchemy sqlalchemy-serializer
```
3.Set up the database (for example, SQLite or PostgreSQL) as per your setup. Flask-SQLAlchemy will automatically create tables based on the defined models.

## Models
The models are defined using SQLAlchemy’s ORM (Object-Relational Mapping) and represent three main entities: Restaurant, Pizza, and RestaurantPizza. These models allow you to easily manage relationships and data within your database.

### Restaurant Model
```
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    # Relationship with RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    def to_dict(self, include_pizzas=True):
        result = {'id': self.id, 'name': self.name, 'address': self.address}
        if include_pizzas:
            result['restaurant_pizzas'] = [rp.to_dict(include_restaurant=False, include_pizza=False) for rp in self.restaurant_pizzas]
        return result
```
#### Fields:
  id: Integer, Primary Key
  name: String, Name of the restaurant
  address: String, Address of the restaurant
**Relationship**:A one-to-many relationship with RestaurantPizza (each restaurant can have many pizzas offered).

### Pizza Model
```
class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Relationship with RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def to_dict(self, include_restaurant=False):
        result = {'id': self.id, 'name': self.name, 'ingredients': self.ingredients}
        if include_restaurant:
            result['restaurant_pizzas'] = [rp.to_dict(include_pizza=False, include_restaurant=False) for rp in self.restaurant_pizzas]
        return result
```
Fields:
id: Integer, Primary Key
name: String, Name of the pizza
ingredients: String, List of ingredients in the pizza
Relationship: A one-to-many relationship with RestaurantPizza (each pizza can appear in many restaurants).
RestaurantPizza Model
```
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Foreign Keys
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    # Relationships to Restaurant and Pizza
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', cascade='all, delete-orphan', single_parent=True)
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def to_dict(self, include_restaurant=True, include_pizza=True):
        result = {'id': self.id, 'price': self.price, 'pizza_id': self.pizza_id, 'restaurant_id': self.restaurant_id}
        if include_pizza:
            result['pizza'] = self.pizza.to_dict(include_restaurant=False) if self.pizza else None
        if include_restaurant:
            result['restaurant'] = self.restaurant.to_dict(include_pizzas=False) if self.restaurant else None
        return result
```
Fields:
id: Integer, Primary Key
price: Integer, Price of the pizza at the restaurant
restaurant_id: Foreign Key linking to the Restaurant table
pizza_id: Foreign Key linking to the Pizza table
Relationships: Many-to-one relationships with Restaurant and Pizza (each RestaurantPizza entry links one pizza to one restaurant).
## Relationships
Restaurant ↔ RestaurantPizza: A restaurant can offer many pizzas, and each pizza offered by the restaurant is recorded in the RestaurantPizza model.

Pizza ↔ RestaurantPizza: A pizza can be offered by many restaurants, and each entry in the RestaurantPizza model links a specific pizza to a restaurant.

## Custom Methods
Each model has a to_dict() method which returns a dictionary representation of the model. This is useful for serializing data into JSON format, especially when building APIs.

Restaurant to_dict(): Can optionally include associated pizzas.
Pizza to_dict(): Can optionally include associated restaurants.
RestaurantPizza to_dict(): Can optionally include the associated restaurant and pizza.
## SerializerMixin
The SerializerMixin class is used to easily convert model instances into dictionaries. This is useful for converting models into JSON objects for API responses. You don't have to manually serialize each field; the to_dict() method handles it for you.

```
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"
    # Fields...
    
    def to_dict(self, include_pizzas=True):
    # Return a dictionary with Restaurant's attributes
```
### Example Usage
Here is an example of how you might interact with these models in a Flask application.

Create a New Restaurant
```
new_restaurant = Restaurant(name="Pizzeria", address="123 Pizza Street")
db.session.add(new_restaurant)
db.session.commit()
```
Create a New Pizza
```
new_pizza = Pizza(name="Margherita", ingredients="Cheese, Tomato, Basil")
db.session.add(new_pizza)
db.session.commit()
```
Link a Pizza to a Restaurant

```
restaurant_pizza = RestaurantPizza(price=15, restaurant_id=new_restaurant.id, pizza_id=new_pizza.id)
db.session.add(restaurant_pizza)
db.session.commit()

```
Get All Restaurants with Pizzas
```
restaurants = Restaurant.query.all()
restaurant_data = [restaurant.to_dict() for restaurant in restaurants]
```
Get All Pizzas with Restaurants
```
pizzas = Pizza.query.all()
pizza_data = [pizza.to_dict(include_restaurant=True) for pizza in pizzas]
```
## Running the Application
1.Create a Flask app instance and configure it with the necessary database settings (e.g., SQLite or PostgreSQL).
2.Initialize the app and create the database tables.
Example:
```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
```
To create the tables in your database, run:
```
flask db init
flask db migrate
flask db upgrade
```
## Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

This README structure provides a thorough explanation of how to set up, use, and understand the SQLAlchemy models in the context of a Flask application.
