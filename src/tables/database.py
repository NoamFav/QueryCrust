from sqlalchemy import Column, Integer, String, DateTime, select, func, ForeignKey, Float, create_engine, event, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class CustomerPersonalInformation(Base):
    __tablename__ = 'customer_personal_information'

    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    birthday = Column(DateTime)
    phone_number = Column(Integer)
    gender = Column(String(18))
    previous_orders = Column(Integer)
    age = Column(Integer)

    orders = relationship('CustomerOrders')


@event.listens_for(CustomerPersonalInformation, 'before_insert')
def auto_increment_menu_id(mapper, connection, target):
    # Use SQLAlchemy's select() to query for the max id in the Menu table
    stmt = select(func.max(CustomerPersonalInformation.id))

    # Execute the select statement using the connection
    result = connection.execute(stmt)
    max_id = result.scalar()

    # Assign the new ID by incrementing the max id
    target.id = (max_id + 1) if max_id else 1


class CustomerOrders(Base):
    __tablename__ = 'customer_orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer_personal_information.id'))
    total_cost = Column(Float)
    delivery_eta = Column(DateTime)
    ordered_at = Column(DateTime)
    status = Column(String(10))
    password = Column(String(30))

    customer = relationship('CustomerPersonalInformation', back_populates='orders')
    sub_orders = relationship('SubOrder', back_populates='order')
    delivery = relationship('Delivery', back_populates='order')


class Delivery(Base):
    __tablename__ = 'delivery'

    delivered_by = Column(Integer, ForeignKey('delivery_driver.id'))
    order_id = Column(Integer, ForeignKey('customer_orders.id'), primary_key=True)

    driver = relationship('DeliveryDriver', back_populates='deliveries')
    order = relationship('CustomerOrders', back_populates='delivery')


class DeliveryDriver(Base):
    __tablename__ = 'delivery_driver'

    id = Column(Integer, primary_key=True)
    delivery_area = Column(String(8))
    last_delivery = Column(DateTime)

    deliveries = relationship('Delivery', back_populates='driver')

class Discounts(Base):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True)
    used = Column(Boolean)

class SubOrder(Base):
    __tablename__ = 'sub_order'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('menu.id'))
    order_id = Column(Integer, ForeignKey('customer_orders.id'))

    # links to be able to go from sub-order to order and vice versa
    order = relationship('CustomerOrders', back_populates='sub_orders')
    menu_item = relationship('Menu', back_populates="sub_orders")
    ingredients = relationship("OrderedIngredient", back_populates="customer_orders")


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    price = Column(Float)
    category = Column(String(10))

    sub_orders = relationship('SubOrder', back_populates='menu_item')


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
class OrderedIngredient(Base):
    __tablename__ = 'ordered_pizza_ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_order_id = Column(Integer, ForeignKey('sub_order.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))


    # Relationships
    customer_orders = relationship("SubOrder", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))


    # Relationships
    menu = relationship("Menu")
    ingredient = relationship("Ingredient", back_populates="menus")


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)
    is_vegetarian = Column(Boolean)
    is_vegan = Column(Boolean)

    menus = relationship("PizzaIngredient", back_populates="ingredient")




