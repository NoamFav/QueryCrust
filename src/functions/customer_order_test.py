from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

import mysql.connector
from src.tables.base import Base


from src.functions.customer_order_utility import OrderContainer
from src.tables.customer_personal_information import CustomerPersonalInformation
from src.tables.menu import Menu


engine = create_engine(f'mysql+mysqlconnector://root:Savafut1@localhost:3306/querycrust')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
print(Base.metadata.tables.keys())

print("Adding mock data...")
pizza_item = Menu(id=1, name='Margherita', price=10.0, category='pizza')
drink_item = Menu(id=2, name='Coke', price=2.0, category='drink')
new_customer_info = CustomerPersonalInformation(
    address=12345,
    birthday=datetime(2000, 1, 1),
    phone_number=1234567890,
    gender='Male',
    previous_orders=10,
    age=24
)
session.add(pizza_item)
session.add(drink_item)
session.commit()
print("Mock data added: 1 pizza and 1 drink")


order_container = OrderContainer(session=session, customer_id=1)


print("\nCreating a new customer order...")
order_container.create_order()
print(f"Order created with ID: {order_container.order.id}, Status: {order_container.order.status}")

# Step 2: Add a sub-order for a pizza
print("\nAdding a sub-order for pizza (Menu ID: 1)...")
order_container.add_suborder(menu_id=1)
print(f"Sub-order added. Total sub-orders: {len(order_container.sub_orders)}")

# Step 3: Try finalizing the order with a pizza
print("\nFinalizing the order with a pizza...")
try:
    order_container.finalize_order()
    print(f"Order finalized. Order ID: {order_container.order.id}, Total Cost: ${order_container.order.total_cost:.2f}")
except ValueError as e:
    print(f"Error finalizing order: {e}")

# Step 4: Create a new order and try adding only a drink (should fail on validation)
print("\nCreating a new order with only a drink (Menu ID: 2)...")
order_container.create_order()  # New order
order_container.add_suborder(menu_id=2)  # Only a drink

# Step 5: Try finalizing the order (this should fail because there's no pizza)
print("\nFinalizing the order with only a drink (should raise an error)...")
try:
    order_container.finalize_order()
except ValueError as e:
    print(f"Validation error caught: {e}")
