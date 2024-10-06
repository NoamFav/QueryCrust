from app import db
from sqlalchemy import select, func, event
from sqlalchemy.orm import relationship

class CustomerPersonalInformation(db.Model):
    __tablename__ = 'customer_personal_information'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    phone_number = db.Column(db.String(15))
    gender = db.Column(db.String(18))
    previous_orders = db.Column(db.Integer)
    age = db.Column(db.Integer)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    orders = relationship('CustomerOrders')

    def __init__(self, address, birthday, phone_number, gender, previous_orders, age, name, email):
        self.address = address
        self.birthday = birthday
        self.phone_number = phone_number
        self.gender = gender
        self.previous_orders = previous_orders
        self.age = age
        self.name = name
        self.email = email


@event.listens_for(CustomerPersonalInformation, 'before_insert')
def auto_increment_menu_id(mapper, connection, target):
    # Use SQLAlchemy's select() to query for the max id in the Menu table
    stmt = select(func.max(CustomerPersonalInformation.id))

    # Execute the select statement using the connection
    result = connection.execute(stmt)
    max_id = result.scalar()

    # Assign the new ID by incrementing the max id
    target.id = (max_id + 1) if max_id else 1


class CustomerOrders(db.Model):
    __tablename__ = 'customer_orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_personal_information.id'))
    total_cost = db.Column(db.Float)
    delivery_eta = db.Column(db.DateTime)
    ordered_at = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    password = db.Column(db.String(30))

    customer = relationship('CustomerPersonalInformation', back_populates='orders')
    sub_orders = relationship('SubOrder', back_populates='order')
    delivery = relationship('Delivery', back_populates='order')

    def __init__(self, customer_id, total_cost, ordered_at, status, delivery_eta):
        self.customer_id = customer_id
        self.total_cost = total_cost
        self.status = status
        self.ordered_at = ordered_at
        self.delivery_eta = delivery_eta



class Delivery(db.Model):
    __tablename__ = 'delivery'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivered_by = db.Column(db.Integer, db.ForeignKey('delivery_driver.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('customer_orders.id'))
    assigned_at = db.Column(db.DateTime)
    pizza_count = db.Column(db.Integer, default=1)

    driver = relationship('DeliveryDriver', back_populates='deliveries')
    order = relationship('CustomerOrders', back_populates='delivery')

    def __init__(self, delivered_by, order_id, assigned_at, pizza_count):
        self.delivered_by = delivered_by
        self.order_id = order_id
        self.assigned_at = assigned_at
        self.pizza_count = pizza_count


class DeliveryDriver(db.Model):
    __tablename__ = 'delivery_driver'

    id = db.Column(db.Integer, primary_key=True)
    delivery_area = db.Column(db.String(50))
    last_delivery = db.Column(db.DateTime)

    deliveries = relationship('Delivery', back_populates='driver')

    def __init__(self, delivery_area, last_delivery):
        self.delivery_area = delivery_area
        self.last_delivery = last_delivery

class Discounts(db.Model):
    __tablename__ = 'discounts'

    id = db.Column(db.Integer, primary_key=True)
    used = db.Column(db.Boolean)

class SubOrder(db.Model):
    __tablename__ = 'sub_order'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('customer_orders.id'))

    # links to be able to go from sub-order to order and vice versa
    order = relationship('CustomerOrders', back_populates='sub_orders')
    menu_item = relationship('Menu', back_populates="sub_orders")
    ingredients = relationship("OrderedIngredient", back_populates="customer_orders")

    def __init__(self, item_id, order_id):
        self.item_id = item_id
        self.order_id = order_id


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    price = db.Column(db.Float)
    category = db.Column(db.String(10))

    sub_orders = relationship('SubOrder', back_populates='menu_item')

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def calculate_total_price(self, session):
        # Get all ingredients for this menu item
        ingredients = session.query(Ingredient).join(PizzaIngredient).filter(PizzaIngredient.menu_id == self.id).all()

        # Calculate the total base cost including the menu item's price
        total_base_cost = float(self.price) + sum(float(ingredient.price) for ingredient in ingredients)
    
        # Apply a 40% profit margin
        price_with_profit = total_base_cost * 1.4

        # Add 9% VAT
        final_price = price_with_profit * 1.09

        return round(float(final_price), 2)  # Ensuring the final_price is cast to float before rounding
    
    def is_vegetarian(self, session):
        ingredients = session.query(Ingredient).join(PizzaIngredient).filter(PizzaIngredient.menu_id == self.id).all()
        return all(ingredient.is_vegetarian for ingredient in ingredients)

    def is_vegan(self, session):
        ingredients = session.query(Ingredient).join(PizzaIngredient).filter(PizzaIngredient.menu_id == self.id).all()
        return all(ingredient.is_vegan for ingredient in ingredients)


@event.listens_for(Menu, 'before_insert')
def set_menu_id(mapper, connection, target):
    # Define category codes
    category_codes = {'pizza': 1, 'drink': 2, 'dessert': 3}
    category_code = category_codes.get(target.category.lower())

    if category_code is None:
        raise ValueError('Invalid category')

    # Calculate the ID range based on category
    start_id = category_code * 1000
    end_id = start_id + 999

    # Use SQLAlchemy's select() to query for the max id in the range
    stmt = select(func.max(Menu.id)).where(Menu.id.between(start_id, end_id))

    # Execute the select statement using the connection
    result = connection.execute(stmt)
    max_id = result.scalar()

    # Assign the new ID
    target.id = (max_id + 1) if max_id else (start_id + 1)


# Association table for many-to-many relationship between Menu and Ingredient
class OrderedIngredient(db.Model):
    __tablename__ = 'ordered_pizza_ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub_order_id = db.Column(db.Integer, db.ForeignKey('sub_order.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    action = db.Column(db.String(5))

    # Relationships
    customer_orders = relationship("SubOrder", back_populates="ingredients")
    ingredient = relationship("Ingredient")

    def __init__(self, sub_order_id, ingredient_id, action):
        self.sub_order_id = sub_order_id
        self.ingredient_id = ingredient_id
        self.action = action


class PizzaIngredient(db.Model):
    __tablename__ = 'pizza_ingredient'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))


    # Relationships
    menu = relationship("Menu")
    ingredient = relationship("Ingredient", back_populates="menus")


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float)
    is_vegetarian = db.Column(db.Boolean)
    is_vegan = db.Column(db.Boolean)

    menus = relationship("PizzaIngredient", back_populates="ingredient")




