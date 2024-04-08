from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pizzas = relationship('Pizza', secondary='restaurant_pizza')


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    restaurants = relationship('Restaurant', secondary='restaurant_pizza')


class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

# Route to get all restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    # Query all the data in restaurants
    restaurants = Restaurant.query.all()
    restaurants_list = []

    # Iterate through the Queried data and store it as JSON
    # Store the data in the restaurants as a dictionary
    for restaurant in restaurants:
        restaurants_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }

        # Append the dictionary to the list
        # Converts the data into a JSON
        restaurants_list.append(restaurants_data)
    return jsonify(restaurants_list), 200
    
# Route to get a specific restaurant by its id
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        # Stores the restaurant data as a dictionary
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizza": []
        }

        # Iterate through the pizza details and append it
        for pizza in restaurant.pizzas:
            pizza_details = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            restaurant_data["pizza"].append(pizza_details)
        return jsonify(restaurant_data), 200
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    
# Route to delete a restaurant by its id
@app.route('/restaurants/<int:id>', methods=["DELETE"])
def delete_restaurant(id):

    restaurant = Restaurant.query.get(id)

    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    

# Route to get all pizzas
@app.route('/pizzas', methods=["GET"])
def get_pizzas():

    pizzas = Pizza.query.all()
    pizza_data_list = []

    # Iterate through the queried pizza data
    for pizza in pizzas:
        pizza_details = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        pizza_data_list.append(pizza_details)

    return jsonify(pizza_data_list), 200


# Route to create a new restaurant pizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizzas():
    data = request.get_json()
    price = data.get("price")
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get("restaurant_id")

    # Confirm if all data is provided
    if not all([price, pizza_id, restaurant_id]):
        return jsonify({"error": "Missing required fields."}), 400
    
    # Check if pizza and restaurant both exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({"error": ["Pizza or Restaurant not found"]}), 404
    
    # Create PizzaRestaurant
    pizza_restaurant = RestaurantPizza(
        price = price,
        pizza_id = pizza_id,
        restaurant_id = restaurant_id
    )

    db.session.add(pizza_restaurant)
    db.session.commit()

    pizza_details = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }

    return jsonify(pizza_details), 201


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

