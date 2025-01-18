from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Metadata configuration for SQLAlchemy
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize the SQLAlchemy instance
db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # Relationship to RestaurantPizza, with cascading deletes
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Restaurant {self.name}>"

    def to_dict(self, include_pizzas=True):  # Default is to include restaurant_pizzas
        """ Return the dictionary representation of a Restaurant. Optionally include restaurant_pizzas."""
        result = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

        if include_pizzas:
            # Include related restaurant_pizzas (exclude nested restaurant or pizza data)
            result['restaurant_pizzas'] = [rp.to_dict(include_restaurant=False, include_pizza=False) for rp in self.restaurant_pizzas]

        return result


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # Relationship to RestaurantPizza
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

    def to_dict(self, include_restaurant=False):
        """ Return the dictionary representation of a Pizza. Optionally include restaurant_pizzas."""
        result = {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

        if include_restaurant:
            # Include related restaurant_pizzas (exclude nested pizza or restaurant data)
            result['restaurant_pizzas'] = [rp.to_dict(include_pizza=False, include_restaurant=False) for rp in self.restaurant_pizzas]

        return result

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Foreign keys to restaurants and pizzas
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    # Relationships to both Restaurant and Pizza models
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', cascade='all, delete-orphan', single_parent=True)
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        """ Ensures that the price is between 1 and 30 inclusive. """
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"

    def to_dict(self, include_restaurant=True, include_pizza=True):
        """ Return the dictionary representation of a RestaurantPizza. Optionally include pizza and restaurant. """
        result = {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
        }

        # Include pizza if requested
        if include_pizza:
            result['pizza'] = self.pizza.to_dict(include_restaurant=False) if self.pizza else None

        # Include restaurant if requested
        if include_restaurant:
            result['restaurant'] = self.restaurant.to_dict(include_pizzas=False) if self.restaurant else None

        return result
