# db_seed.py
from app import create_app
from models import db
from models.database import Menu, Ingredient, PizzaIngredient, DeliveryDriver
from sqlalchemy.orm import sessionmaker

app = create_app()

# Use app.app_context() to ensure the app context is available
with app.app_context():
    # Create a new session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    # Create ingredients
    ingredients_data = [
        {'name': 'Cheese', 'price': 0.50, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Tomato Sauce', 'price': 0.25, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Bell Peppers', 'price': 0.30, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Olives', 'price': 0.35, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Mushrooms', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Onions', 'price': 0.45, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Blue Cheese', 'price': 0.50, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Cheddar Cheese', 'price': 0.45, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Mozzarella', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Feta Cheese', 'price': 0.60, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Parmesan Cheese', 'price': 0.70, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Gorgonzola', 'price': 0.75, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Ricotta', 'price': 0.80, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Garlic', 'price': 0.25, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Red Onion', 'price': 0.30, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'BBQ Sauce', 'price': 0.35, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Buffalo Sauce', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Pesto', 'price': 0.45, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Alfredo Sauce', 'price': 0.50, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Pasta Sauce', 'price': 0.55, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Peanut Sauce', 'price': 0.55, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Firecracker Sauce', 'price': 0.60, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Olive Oil', 'price': 0.60, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Truffle Oil', 'price': 0.65, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Sriracha Sauce', 'price': 0.70, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Ranch Dressing', 'price': 0.75, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Cilantro', 'price': 0.15, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Spinach', 'price': 0.30, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Kale', 'price': 0.35, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Arugula', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Chicken', 'price': 1.00, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Turkey', 'price': 0.90, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Duck', 'price': 1.10, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Pork', 'price': 0.95, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Cajun Chicken', 'price': 1.20, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Calamari', 'price': 1.20, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Sausage', 'price': 0.90, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Pepperoni', 'price': 0.70, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Salami', 'price': 0.85, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Pancetta', 'price': 0.80, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Chorizo', 'price': 0.95, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Ham', 'price': 0.75, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Bacon', 'price': 0.80, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Beef', 'price': 1.00, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Prawns', 'price': 1.10, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Ground Beef', 'price': 1.10, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Kebab Meat', 'price': 1.20, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Shrimp', 'price': 1.30, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Crab', 'price': 1.40, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Pulled Pork', 'price': 1.50, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Lamb', 'price': 1.60, 'is_vegetarian': False, 'is_vegan': False},
        {'name': 'Pickles', 'price': 0.25, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Tomatoes', 'price': 0.30, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Lettuce', 'price': 0.20, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Artichokes', 'price': 0.75, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Zucchini', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Jalapeños', 'price': 0.50, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Broccoli', 'price': 0.45, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Pesto', 'price': 0.60, 'is_vegetarian': True, 'is_vegan': False},
        {'name': 'Veggies', 'price': 0.55, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Lentils', 'price': 0.65, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Sun-Dried Tomatoes', 'price': 0.70, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Basil', 'price': 0.20, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Oregano', 'price': 0.15, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Chili Flakes', 'price': 0.10, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Capers', 'price': 0.55, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Fennel', 'price': 0.45, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Eggplant', 'price': 0.50, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Celery', 'price': 0.30, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Cauliflower', 'price': 0.40, 'is_vegetarian': True, 'is_vegan': True},
        {'name': 'Zaatar', 'price': 0.35, 'is_vegetarian': True, 'is_vegan': True},
    ]

    # Add ingredients to the session
    for ingredient_data in ingredients_data:
        existing_ingredient = session.query(Ingredient).filter_by(name=ingredient_data['name']).first()
        if existing_ingredient is None:
            ingredient = Ingredient(**ingredient_data)
            session.add(ingredient)

    session.commit()

    # Map ingredient names to their IDs for easy reference
    ingredient_dict = {ingredient.name: ingredient.id for ingredient in session.query(Ingredient).all()}

    # Create menu items (pizzas)
    pizzas_da = [
        {'name': 'BBQ Chicken', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Four Cheese', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Pesto Chicken', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Buffalo Chicken', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Mediterranean Veggie', 'price': 10.99, 'category': 'pizza'},
        {'name': 'Spinach and Feta', 'price': 10.49, 'category': 'pizza'},
        {'name': 'Chicken Alfredo', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Seafood Pizza', 'price': 13.49, 'category': 'pizza'},
        {'name': 'Thai Chicken Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Cheeseburger Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Taco Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Hawaiian Delight', 'price': 12.49, 'category': 'pizza'},  # Hawaiian without pineapple because it's a crime
        {'name': 'Caprese Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Fajita Chicken Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Truffle Mushroom Pizza', 'price': 13.99, 'category': 'pizza'},
        {'name': 'BBQ Pulled Pork Pizza', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Ranch Chicken Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Cheesy Garlic Pizza', 'price': 9.49, 'category': 'pizza'},
        {'name': 'Greek Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Spinach and Artichoke Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Sausage and Peppers Pizza', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Veggie Supreme', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Wild Mushroom Pizza', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Smoky BBQ Veggie', 'price': 10.99, 'category': 'pizza'},
        {'name': 'Lentil and Spinach Pizza', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Roasted Veggie Pizza', 'price': 10.99, 'category': 'pizza'},
        {'name': 'Pepperoni and Jalapeño', 'price': 10.99, 'category': 'pizza'},
        {'name': 'Zaatar Chicken Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Alfredo Shrimp Pizza', 'price': 13.49, 'category': 'pizza'},
        {'name': 'Pesto Veggie Pizza', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Buffalo Veggie Pizza', 'price': 11.49, 'category': 'pizza'},
        {'name': 'Sriracha Chicken Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Carbonara Pizza', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Truffle Chicken Pizza', 'price': 13.49, 'category': 'pizza'},
        {'name': 'Ratatouille Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Prawn and Chorizo Pizza', 'price': 14.99, 'category': 'pizza'},
        {'name': 'Beef Stroganoff Pizza', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Cajun Chicken Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Mediterranean Lamb Pizza', 'price': 13.49, 'category': 'pizza'},
        {'name': 'Garlic and Herb Chicken Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'Eggplant Parmesan Pizza', 'price': 11.99, 'category': 'pizza'},
        {'name': 'Buffalo Cauliflower Pizza', 'price': 10.99, 'category': 'pizza'},
        {'name': 'Roasted Garlic Pizza', 'price': 9.99, 'category': 'pizza'},
        {'name': 'Prawn Scampi Pizza', 'price': 14.49, 'category': 'pizza'},
        {'name': 'Pork and Pineapple', 'price': 12.99, 'category': 'pizza'},
        {'name': 'Firecracker Chicken Pizza', 'price': 12.49, 'category': 'pizza'},
        {'name': 'margherita', 'price': 8.99, 'category': 'pizza'},
        {'name': 'pepperoni', 'price': 9.49, 'category': 'pizza'},
        {'name': 'veggie delight', 'price': 10.49, 'category': 'pizza'},
        {'name': 'meat lovers', 'price': 12.99, 'category': 'pizza'},
    ]
    # Add pizzas to the session and get their IDs
    pizzas = [Menu(**data) for data in pizzas_da]
    session.add_all(pizzas)
    session.commit()

    # Map pizza names to their IDs
    pizza_dict = {pizza.name: pizza.id for pizza in pizzas}

    # Associate ingredients with pizzas
    pizza_ingredients = []

    # Associate ingredients with pizzas
    pizza_ingredients.extend([
    # BBQ Chicken Pizza
    PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['BBQ Sauce']),
    PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['Red Onion']),
    PizzaIngredient(menu_id=pizzas[0].id, ingredient_id=ingredient_dict['Cheddar Cheese']),

    # Four Cheese Pizza
    PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Cheddar Cheese']),
    PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Blue Cheese']),
    PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Mozzarella']),
    PizzaIngredient(menu_id=pizzas[1].id, ingredient_id=ingredient_dict['Feta Cheese']),

    # Pesto Chicken Pizza
    PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Pesto']),
    PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Spinach']),
    PizzaIngredient(menu_id=pizzas[2].id, ingredient_id=ingredient_dict['Mozzarella']),

    # Buffalo Chicken Pizza
    PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Buffalo Sauce']),
    PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Blue Cheese']),
    PizzaIngredient(menu_id=pizzas[3].id, ingredient_id=ingredient_dict['Celery']),

    # Mediterranean Veggie Pizza
    PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Olives']),
    PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Artichokes']),
    PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Spinach']),
    PizzaIngredient(menu_id=pizzas[4].id, ingredient_id=ingredient_dict['Feta Cheese']),

    # Spinach and Feta Pizza
    PizzaIngredient(menu_id=pizzas[5].id, ingredient_id=ingredient_dict['Spinach']),
    PizzaIngredient(menu_id=pizzas[5].id, ingredient_id=ingredient_dict['Feta Cheese']),
    PizzaIngredient(menu_id=pizzas[5].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[5].id, ingredient_id=ingredient_dict['Mozzarella']),

    # Chicken Alfredo Pizza
    PizzaIngredient(menu_id=pizzas[6].id, ingredient_id=ingredient_dict['Alfredo Sauce']),
    PizzaIngredient(menu_id=pizzas[6].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[6].id, ingredient_id=ingredient_dict['Cheddar Cheese']),

    # Seafood Pizza
    PizzaIngredient(menu_id=pizzas[7].id, ingredient_id=ingredient_dict['Shrimp']),
    PizzaIngredient(menu_id=pizzas[7].id, ingredient_id=ingredient_dict['Crab']),
    PizzaIngredient(menu_id=pizzas[7].id, ingredient_id=ingredient_dict['Garlic']),
    PizzaIngredient(menu_id=pizzas[7].id, ingredient_id=ingredient_dict['Tomato Sauce']),

    # Thai Chicken Pizza
    PizzaIngredient(menu_id=pizzas[8].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[8].id, ingredient_id=ingredient_dict['Peanut Sauce']),
    PizzaIngredient(menu_id=pizzas[8].id, ingredient_id=ingredient_dict['Cilantro']),
    PizzaIngredient(menu_id=pizzas[8].id, ingredient_id=ingredient_dict['Jalapeños']),

    # Cheeseburger Pizza
    PizzaIngredient(menu_id=pizzas[9].id, ingredient_id=ingredient_dict['Ground Beef']),
    PizzaIngredient(menu_id=pizzas[9].id, ingredient_id=ingredient_dict['Cheddar Cheese']),
    PizzaIngredient(menu_id=pizzas[9].id, ingredient_id=ingredient_dict['Pickles']),
    PizzaIngredient(menu_id=pizzas[9].id, ingredient_id=ingredient_dict['Onions']),

    # Taco Pizza
    PizzaIngredient(menu_id=pizzas[10].id, ingredient_id=ingredient_dict['Ground Beef']),
    PizzaIngredient(menu_id=pizzas[10].id, ingredient_id=ingredient_dict['Cheddar Cheese']),
    PizzaIngredient(menu_id=pizzas[10].id, ingredient_id=ingredient_dict['Lettuce']),
    PizzaIngredient(menu_id=pizzas[10].id, ingredient_id=ingredient_dict['Tomatoes']),

    # Hawaiian Delight Pizza
    PizzaIngredient(menu_id=pizzas[11].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[11].id, ingredient_id=ingredient_dict['Cheese']),
    PizzaIngredient(menu_id=pizzas[11].id, ingredient_id=ingredient_dict['Ham']),

    # Caprese Pizza
    PizzaIngredient(menu_id=pizzas[12].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[12].id, ingredient_id=ingredient_dict['Mozzarella']),
    PizzaIngredient(menu_id=pizzas[12].id, ingredient_id=ingredient_dict['Basil']),
    PizzaIngredient(menu_id=pizzas[12].id, ingredient_id=ingredient_dict['Olive Oil']),

    # Fajita Chicken Pizza
    PizzaIngredient(menu_id=pizzas[13].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[13].id, ingredient_id=ingredient_dict['Bell Peppers']),
    PizzaIngredient(menu_id=pizzas[13].id, ingredient_id=ingredient_dict['Onions']),
    PizzaIngredient(menu_id=pizzas[13].id, ingredient_id=ingredient_dict['BBQ Sauce']),

    # Truffle Mushroom Pizza
    PizzaIngredient(menu_id=pizzas[14].id, ingredient_id=ingredient_dict['Truffle Oil']),
    PizzaIngredient(menu_id=pizzas[14].id, ingredient_id=ingredient_dict['Mushrooms']),
    PizzaIngredient(menu_id=pizzas[14].id, ingredient_id=ingredient_dict['Garlic']),
    PizzaIngredient(menu_id=pizzas[14].id, ingredient_id=ingredient_dict['Cheese']),

    # BBQ Pulled Pork Pizza
    PizzaIngredient(menu_id=pizzas[15].id, ingredient_id=ingredient_dict['Pulled Pork']),
    PizzaIngredient(menu_id=pizzas[15].id, ingredient_id=ingredient_dict['BBQ Sauce']),
    PizzaIngredient(menu_id=pizzas[15].id, ingredient_id=ingredient_dict['Red Onion']),
    PizzaIngredient(menu_id=pizzas[15].id, ingredient_id=ingredient_dict['Cheddar Cheese']),

    # Ranch Chicken Pizza
    PizzaIngredient(menu_id=pizzas[16].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[16].id, ingredient_id=ingredient_dict['Ranch Dressing']),
    PizzaIngredient(menu_id=pizzas[16].id, ingredient_id=ingredient_dict['Cheddar Cheese']),
    
    # Cheesy Garlic Pizza
    PizzaIngredient(menu_id=pizzas[17].id, ingredient_id=ingredient_dict['Garlic']),
    PizzaIngredient(menu_id=pizzas[17].id, ingredient_id=ingredient_dict['Cheddar Cheese']),
    PizzaIngredient(menu_id=pizzas[17].id, ingredient_id=ingredient_dict['Mozzarella']),
    
    # Greek Pizza
    PizzaIngredient(menu_id=pizzas[18].id, ingredient_id=ingredient_dict['Feta Cheese']),
    PizzaIngredient(menu_id=pizzas[18].id, ingredient_id=ingredient_dict['Olives']),
    PizzaIngredient(menu_id=pizzas[18].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    
    # Spinach and Artichoke Pizza
    PizzaIngredient(menu_id=pizzas[19].id, ingredient_id=ingredient_dict['Spinach']),
    PizzaIngredient(menu_id=pizzas[19].id, ingredient_id=ingredient_dict['Artichokes']),
    PizzaIngredient(menu_id=pizzas[19].id, ingredient_id=ingredient_dict['Cheese']),
    
    # Sausage and Peppers Pizza
    PizzaIngredient(menu_id=pizzas[20].id, ingredient_id=ingredient_dict['Sausage']),
    PizzaIngredient(menu_id=pizzas[20].id, ingredient_id=ingredient_dict['Bell Peppers']),
    
    # Veggie Supreme
    PizzaIngredient(menu_id=pizzas[21].id, ingredient_id=ingredient_dict['Olives']),
    PizzaIngredient(menu_id=pizzas[21].id, ingredient_id=ingredient_dict['Spinach']),
    PizzaIngredient(menu_id=pizzas[21].id, ingredient_id=ingredient_dict['Mushrooms']),
    
    # Wild Mushroom Pizza
    PizzaIngredient(menu_id=pizzas[22].id, ingredient_id=ingredient_dict['Mushrooms']),
    PizzaIngredient(menu_id=pizzas[22].id, ingredient_id=ingredient_dict['Truffle Oil']),
    
    # Smoky BBQ Veggie
    PizzaIngredient(menu_id=pizzas[23].id, ingredient_id=ingredient_dict['BBQ Sauce']),
    PizzaIngredient(menu_id=pizzas[23].id, ingredient_id=ingredient_dict['Veggies']),
    
    # Lentil and Spinach Pizza
    PizzaIngredient(menu_id=pizzas[24].id, ingredient_id=ingredient_dict['Lentils']),
    PizzaIngredient(menu_id=pizzas[24].id, ingredient_id=ingredient_dict['Spinach']),
    
    # Roasted Veggie Pizza
    PizzaIngredient(menu_id=pizzas[25].id, ingredient_id=ingredient_dict['Zucchini']),
    PizzaIngredient(menu_id=pizzas[25].id, ingredient_id=ingredient_dict['Olives']),
    
    # Pepperoni and Jalapeño
    PizzaIngredient(menu_id=pizzas[26].id, ingredient_id=ingredient_dict['Pepperoni']),
    PizzaIngredient(menu_id=pizzas[26].id, ingredient_id=ingredient_dict['Jalapeños']),
    
    # Zaatar Chicken Pizza
    PizzaIngredient(menu_id=pizzas[27].id, ingredient_id=ingredient_dict['Zaatar']),
    PizzaIngredient(menu_id=pizzas[27].id, ingredient_id=ingredient_dict['Chicken']),
    
    # Alfredo Shrimp Pizza
    PizzaIngredient(menu_id=pizzas[28].id, ingredient_id=ingredient_dict['Shrimp']),
    PizzaIngredient(menu_id=pizzas[28].id, ingredient_id=ingredient_dict['Alfredo Sauce']),
    
    # Pesto Veggie Pizza
    PizzaIngredient(menu_id=pizzas[29].id, ingredient_id=ingredient_dict['Pesto']),
    PizzaIngredient(menu_id=pizzas[29].id, ingredient_id=ingredient_dict['Veggies']),
    
    # Buffalo Veggie Pizza
    PizzaIngredient(menu_id=pizzas[30].id, ingredient_id=ingredient_dict['Buffalo Sauce']),
    PizzaIngredient(menu_id=pizzas[30].id, ingredient_id=ingredient_dict['Veggies']),
    
    # Sriracha Chicken Pizza
    PizzaIngredient(menu_id=pizzas[31].id, ingredient_id=ingredient_dict['Chicken']),
    PizzaIngredient(menu_id=pizzas[31].id, ingredient_id=ingredient_dict['Sriracha Sauce']),
    
    # Carbonara Pizza
    PizzaIngredient(menu_id=pizzas[32].id, ingredient_id=ingredient_dict['Pasta Sauce']),
    PizzaIngredient(menu_id=pizzas[32].id, ingredient_id=ingredient_dict['Pancetta']),
    
    # Truffle Chicken Pizza
    PizzaIngredient(menu_id=pizzas[33].id, ingredient_id=ingredient_dict['Truffle Oil']),
    PizzaIngredient(menu_id=pizzas[33].id, ingredient_id=ingredient_dict['Chicken']),
    
    # Ratatouille Pizza
    PizzaIngredient(menu_id=pizzas[34].id, ingredient_id=ingredient_dict['Zucchini']),
    PizzaIngredient(menu_id=pizzas[34].id, ingredient_id=ingredient_dict['Eggplant']),
    
    # Prawn and Chorizo Pizza
    PizzaIngredient(menu_id=pizzas[35].id, ingredient_id=ingredient_dict['Chorizo']),
    PizzaIngredient(menu_id=pizzas[35].id, ingredient_id=ingredient_dict['Prawns']),
    
    # Beef Stroganoff Pizza
    PizzaIngredient(menu_id=pizzas[36].id, ingredient_id=ingredient_dict['Beef']),
    PizzaIngredient(menu_id=pizzas[36].id, ingredient_id=ingredient_dict['Mushrooms']),
    
    # Cajun Chicken Pizza
    PizzaIngredient(menu_id=pizzas[37].id, ingredient_id=ingredient_dict['Cajun Chicken']),
    
    # Mediterranean Lamb Pizza
    PizzaIngredient(menu_id=pizzas[38].id, ingredient_id=ingredient_dict['Lamb']),
    
    # Garlic and Herb Chicken Pizza
    PizzaIngredient(menu_id=pizzas[39].id, ingredient_id=ingredient_dict['Garlic']),
    
    # Eggplant Parmesan Pizza
    PizzaIngredient(menu_id=pizzas[40].id, ingredient_id=ingredient_dict['Eggplant']),
    
    # Buffalo Cauliflower Pizza
    PizzaIngredient(menu_id=pizzas[41].id, ingredient_id=ingredient_dict['Cauliflower']),
    
    # Roasted Garlic Pizza
    PizzaIngredient(menu_id=pizzas[42].id, ingredient_id=ingredient_dict['Garlic']),
    
    # Prawn Scampi Pizza
    PizzaIngredient(menu_id=pizzas[43].id, ingredient_id=ingredient_dict['Prawns']),
    
    # Firecracker Chicken Pizza
    PizzaIngredient(menu_id=pizzas[44].id, ingredient_id=ingredient_dict['Firecracker Sauce']),

    # Margherita Pizza
    PizzaIngredient(menu_id=pizzas[45].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[45].id, ingredient_id=ingredient_dict['Cheese']),

    # Pepperoni Pizza
    PizzaIngredient(menu_id=pizzas[46].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[46].id, ingredient_id=ingredient_dict['Pepperoni']),
    PizzaIngredient(menu_id=pizzas[46].id, ingredient_id=ingredient_dict['Cheese']),

    # Veggie Delight Pizza
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Veggies']),
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Cheese']),
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Olives']),
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Onions']),
    PizzaIngredient(menu_id=pizzas[47].id, ingredient_id=ingredient_dict['Bell Peppers']),

    # Meat Lovers Pizza
    PizzaIngredient(menu_id=pizzas[48].id, ingredient_id=ingredient_dict['Cheese']),
    PizzaIngredient(menu_id=pizzas[48].id, ingredient_id=ingredient_dict['Tomato Sauce']),
    PizzaIngredient(menu_id=pizzas[48].id, ingredient_id=ingredient_dict['Pepperoni']),
    PizzaIngredient(menu_id=pizzas[48].id, ingredient_id=ingredient_dict['Bacon']),
    PizzaIngredient(menu_id=pizzas[48].id, ingredient_id=ingredient_dict['Ham']),

    ])
    
    session.add_all(pizza_ingredients)
    session.commit()

    # Create menu items (drinks)
    drinks_data = [
        {'name': 'Coke', 'price': 1.99, 'category': 'drink'},
        {'name': 'Diet Coke', 'price': 1.99, 'category': 'drink'},
        {'name': 'Sprite', 'price': 1.99, 'category': 'drink'},
        {'name': 'Water', 'price': 1.49, 'category': 'drink'},
        {'name': 'Orange Juice', 'price': 2.49, 'category': 'drink'},
        {'name': 'Lemonade', 'price': 2.29, 'category': 'drink'},
        {'name': 'Iced Tea', 'price': 2.49, 'category': 'drink'},
        {'name': 'Root Beer', 'price': 2.59, 'category': 'drink'},
        {'name': 'Fanta', 'price': 1.99, 'category': 'drink'},
        {'name': 'Dr. Pepper', 'price': 2.29, 'category': 'drink'},
        {'name': 'Peach Iced Tea', 'price': 2.59, 'category': 'drink'},
        {'name': 'Mango Juice', 'price': 2.99, 'category': 'drink'},
        {'name': 'Ginger Ale', 'price': 2.29, 'category': 'drink'},
        {'name': 'Lemon-Lime Soda', 'price': 1.89, 'category': 'drink'},
        {'name': 'Cranberry Juice', 'price': 2.49, 'category': 'drink'},
        {'name': 'Berry Smoothie', 'price': 3.49, 'category': 'drink'},
        {'name': 'Tropical Punch', 'price': 2.49, 'category': 'drink'},
        {'name': 'Chocolate Milk', 'price': 2.79, 'category': 'drink'},
        {'name': 'Strawberry Lemonade', 'price': 2.99, 'category': 'drink'},
        {'name': 'Sparkling Water', 'price': 1.99, 'category': 'drink'},
        {'name': 'Apple Juice', 'price': 2.29, 'category': 'drink'},
        {'name': 'Cold Brew Coffee', 'price': 3.49, 'category': 'drink'},
        {'name': 'Vanilla Milkshake', 'price': 3.99, 'category': 'drink'},
        {'name': 'Banana Smoothie', 'price': 3.49, 'category': 'drink'},
        {'name': 'Pepsi', 'price': 1.99, 'category': 'drink'},
        {'name': 'Diet Coke', 'price': 1.99, 'category': 'drink'},
        {'name': 'Root Beer Float', 'price': 3.49, 'category': 'drink'},
    ]

    for drink_data in drinks_data:
        existing_drink = session.query(Menu).filter_by(name=drink_data['name']).first()
        if existing_drink is None:
            drink = Menu(**drink_data)
            session.add(drink)

    session.commit()

    # Create menu items (desserts)
    desserts_data = [
        {'name': 'Cheesecake', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Tiramisu', 'price': 5.49, 'category': 'dessert'},
        {'name': 'Apple Pie', 'price': 4.49, 'category': 'dessert'},
        {'name': 'Ice Cream', 'price': 3.49, 'category': 'dessert'},
        {'name': 'Chocolate Cake', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Brownie', 'price': 3.49, 'category': 'dessert'},
        {'name': 'Panna Cotta', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Fruit Salad', 'price': 3.99, 'category': 'dessert'},
        {'name': 'Cupcakes', 'price': 3.49, 'category': 'dessert'},
        {'name': 'Lemon Tart', 'price': 4.49, 'category': 'dessert'},
        {'name': 'Carrot Cake', 'price': 5.49, 'category': 'dessert'},
        {'name': 'Banoffee Pie', 'price': 5.99, 'category': 'dessert'},
        {'name': 'Chocolate Mousse', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Rice Pudding', 'price': 3.29, 'category': 'dessert'},
        {'name': 'Eclair', 'price': 3.99, 'category': 'dessert'},
        {'name': 'Baklava', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Pavlova', 'price': 4.49, 'category': 'dessert'},
        {'name': 'Mango Sticky Rice', 'price': 4.99, 'category': 'dessert'},
        {'name': 'Cookies', 'price': 2.99, 'category': 'dessert'},
        {'name': 'Chocolate Fondue', 'price': 6.49, 'category': 'dessert'},
        {'name': 'Creme Brulee', 'price': 5.99, 'category': 'dessert'},
        {'name': 'Peach Cobbler', 'price': 4.49, 'category': 'dessert'},
        {'name': 'S\'mores', 'price': 3.99, 'category': 'dessert'},
        {'name': 'Vanilla Pudding', 'price': 2.99, 'category': 'dessert'},
    ]
    for dessert_data in desserts_data:
        existing_dessert = session.query(Menu).filter_by(name=dessert_data['name']).first()
        if existing_dessert is None:
            dessert = Menu(**dessert_data)
            session.add(dessert)

    session.commit()

    # Create menu items (extras)
    extras_data = [
        {'name': 'Garlic Bread', 'price': 2.99, 'category': 'extra'},
        {'name': 'Cheese Bread', 'price': 3.49, 'category': 'extra'},
        {'name': 'Wings', 'price': 6.99, 'category': 'extra'},
        {'name': 'Garlic Knots', 'price': 3.49, 'category': 'extra'},
        {'name': 'Salad', 'price': 4.99, 'category': 'extra'},
        {'name': 'Soup', 'price': 3.99, 'category': 'extra'},
        {'name': 'Mac and Cheese', 'price': 5.49, 'category': 'extra'},
        {'name': 'Fries', 'price': 2.99, 'category': 'extra'},
        {'name': 'Onion Rings', 'price': 3.99, 'category': 'extra'},
        {'name': 'Nachos', 'price': 5.99, 'category': 'extra'},
        {'name': 'Breadsticks', 'price': 4.49, 'category': 'extra'},
        {'name': 'Dipping Sauces', 'price': 0.99, 'category': 'extra'},
        {'name': 'Stuffed Jalapeños', 'price': 5.49, 'category': 'extra'},
        {'name': 'Caprese Salad', 'price': 5.99, 'category': 'extra'},
        {'name': 'Potato Wedges', 'price': 3.99, 'category': 'extra'},
        {'name': 'Cheese Curds', 'price': 6.49, 'category': 'extra'},
        {'name': 'Fried Pickles', 'price': 4.99, 'category': 'extra'},
        {'name': 'Shrimp Cocktail', 'price': 8.99, 'category': 'extra'},
        {'name': 'Vegetable Spring Rolls', 'price': 4.49, 'category': 'extra'},
        {'name': 'Buffalo Cauliflower', 'price': 5.99, 'category': 'extra'},
        {'name': 'Chili Cheese Fries', 'price': 6.49, 'category': 'extra'},
        {'name': 'Poutine', 'price': 7.49, 'category': 'extra'},
        {'name': 'Fruit Cup', 'price': 3.49, 'category': 'extra'},
        {'name': 'Hummus and Pita', 'price': 4.99, 'category': 'extra'},
        {'name': 'Meatballs', 'price': 5.49, 'category': 'extra'},
        {'name': 'Mini Tacos', 'price': 6.99, 'category': 'extra'},
    ]
    for extra_data in extras_data:
        existing_extra = session.query(Menu).filter_by(name=extra_data['name']).first()
        if existing_extra is None:
            extra = Menu(**extra_data)
            session.add(extra)

    session.commit()

    print("Database seeded successfully with pizzas, drinks, desserts, and extras!")
