# db_seed.py
from app import create_app
from models import db
from models.database import Menu, Ingredient, PizzaIngredient
from sqlalchemy.orm import sessionmaker

app = create_app()

# Use app.app_context() to ensure the app context is available
with app.app_context():
    # Create a new session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    # Create ingredients
    ingredients = [
        Ingredient(name='Cheese', price=0.50, is_vegetarian=True, is_vegan=False),
        Ingredient(name='Tomato Sauce', price=0.30, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Pepperoni', price=0.70, is_vegetarian=False, is_vegan=False),
        Ingredient(name='Mushrooms', price=0.60, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Olives', price=0.40, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Onions', price=0.35, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Bacon', price=0.80, is_vegetarian=False, is_vegan=False),
        Ingredient(name='Bell Peppers', price=0.50, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Pineapple', price=0.55, is_vegetarian=True, is_vegan=True),
        Ingredient(name='Ham', price=0.75, is_vegetarian=False, is_vegan=False),
    ]

    # Add ingredients to the session
    session.add_all(ingredients)
    session.commit()

    # Map ingredient names to their IDs for easy reference
    ingredient_dict = {ingredient.name: ingredient.id for ingredient in ingredients}

    # Create menu items (pizzas)
    pizzas = [
        Menu(name='Margherita', price=8.99, category='pizza'),
        Menu(name='Pepperoni Pizza', price=9.99, category='pizza'),
        Menu(name='Veggie Delight', price=10.99, category='pizza'),
        Menu(name='Hawaiian Pizza', price=11.49, category='pizza'),
        Menu(name='Meat Lovers', price=12.49, category='pizza'),
    ]

    # Add pizzas to the session
    session.add_all(pizzas)
    session.commit()

    # Associate ingredients with pizzas
    pizza_ingredients = []

    # Margherita Pizza Ingredients
    pizza_ingredients.extend([
        PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['Cheese']),
        PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    ])

    # Pepperoni Pizza Ingredients
    pizza_ingredients.extend([
        PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Cheese']),
        PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Tomato Sauce']),
        PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Pepperoni']),
    ])

    # Veggie Delight Pizza Ingredients
    pizza_ingredients.extend([
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Cheese']),
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Tomato Sauce']),
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Mushrooms']),
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Olives']),
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Onions']),
        PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Bell Peppers']),
    ])

    # Hawaiian Pizza Ingredients
    pizza_ingredients.extend([
        PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Cheese']),
        PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Tomato Sauce']),
        PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Ham']),
        PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Pineapple']),
    ])

    # Meat Lovers Pizza Ingredients
    pizza_ingredients.extend([
        PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Cheese']),
        PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Tomato Sauce']),
        PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Pepperoni']),
        PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Bacon']),
        PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Ham']),
    ])

    # Add pizza ingredients to the session
    session.add_all(pizza_ingredients)
    session.commit()

    # Create menu items (drinks)
    drinks = [
        Menu(name='Coca-Cola', price=1.99, category='drink'),
        Menu(name='Sprite', price=1.99, category='drink'),
        Menu(name='Water', price=1.49, category='drink'),
        Menu(name='Orange Juice', price=2.49, category='drink'),
        Menu(name='Lemonade', price=2.29, category='drink'),
    ]

    session.add_all(drinks)
    session.commit()

    # Create menu items (desserts)
    desserts = [
        Menu(name='Chocolate Cake', price=4.99, category='dessert'),
        Menu(name='Ice Cream', price=3.99, category='dessert'),
        Menu(name='Cheesecake', price=5.49, category='dessert'),
        Menu(name='Apple Pie', price=4.49, category='dessert'),
        Menu(name='Tiramisu', price=5.99, category='dessert'),
    ]

    session.add_all(desserts)
    session.commit()

    # Create menu items (extras)
    extras = [
        Menu(name='Garlic Bread', price=3.49, category='extra'),
        Menu(name='Chicken Wings', price=6.99, category='extra'),
        Menu(name='French Fries', price=2.99, category='extra'),
        Menu(name='Mozzarella Sticks', price=5.49, category='extra'),
        Menu(name='Salad', price=4.29, category='extra'),
    ]

    session.add_all(extras)
    session.commit()

    print("Database seeded successfully with pizzas, drinks, desserts, and extras!")
