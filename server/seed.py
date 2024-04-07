from app import app, db, Restaurant, Pizza, RestaurantPizza

if __name__ == "__main__":
    # Create app context
    with app.app_context():
        # Create Restaurants
        restaurant1 = Restaurant(name="PizzaInn", address="GMoi Avenue, 5th Avenue")
        restaurant2 = Restaurant(name="Galitos", address="Westgate Mall, Mwanzi Road, Nrb 100")

        # Create Pizzas
        pizza1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
        pizza2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

        # Add Restaurants and Pizzas to the session
        db.session.add_all([restaurant1, restaurant2, pizza1, pizza2])
        db.session.commit()

        # Create RestaurantPizzas (Linking Pizzas to Restaurants)
        restaurant_pizza1 = RestaurantPizza(price=10, restaurant_id=restaurant1.id, pizza_id=pizza1.id)
        restaurant_pizza2 = RestaurantPizza(price=12, restaurant_id=restaurant1.id, pizza_id=pizza2.id)
        restaurant_pizza3 = RestaurantPizza(price=11, restaurant_id=restaurant2.id, pizza_id=pizza1.id)
        restaurant_pizza4 = RestaurantPizza(price=13, restaurant_id=restaurant2.id, pizza_id=pizza2.id)

        # Add RestaurantPizzas to the session
        db.session.add_all([restaurant_pizza1, restaurant_pizza2, restaurant_pizza3, restaurant_pizza4])
        db.session.commit()


