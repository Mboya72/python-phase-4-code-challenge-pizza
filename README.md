# Flask SQLAlchemy Models
This README provides an overview of the SQLAlchemy models used for a restaurant and pizza application. The application is built using Flask and SQLAlchemy and includes models for restaurants, pizzas, and the relationships between them.

## Installation
To use the models, make sure you have the following dependencies installed:

1.Flask

2.Flask-SQLAlchemy

3.SQLAlchemy

4.sqlalchemy_serializer

You can install the necessary dependencies using pip:

pip install Flask Flask-SQLAlchemy SQLAlchemy sqlalchemy-serializer

### Models Overview

This application uses SQLAlchemy to define the following models:

Restaurant
Pizza
RestaurantPizza (A relationship model to link restaurants and pizzas with additional attributes)
Each model also uses the SerializerMixin to easily convert objects to JSON-like dictionaries for API responses.

Metadata Configuration

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
The MetaData object configures naming conventions for foreign keys. This is helpful for making sure the foreign key constraint names are consistent across the database.

SQLAlchemy Initialization

db = SQLAlchemy(metadata=metadata)
The SQLAlchemy instance is initialized with the custom metadata configuration.

