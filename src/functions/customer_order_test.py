from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.tables.database import *
from customer_order_utility import *
from gui_integration import *

## warning: this is all bullshit spun up by chatgpt to give this code a little runaround

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gui_integration import get_menu_items_by_starting_id, get_non_completed_orders, create_customer_order



# Set up the in-memory database
def setup_database():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Add some test menu items and ingredients
def add_menu_items_and_ingredients(session):
    print("Adding menu items and ingredients to the database...")
    pizza_item = Menu(name='Margherita', price=10.0, category='pizza')
    drink_item = Menu(name='Coke', price=2.0, category='drink')

    # Add some ingredients for pizzas
    cheese = Ingredient(name="Cheese")
    tomato = Ingredient(name="Tomato")

    session.add(pizza_item)
    session.add(drink_item)
    session.add(cheese)
    session.add(tomato)
    session.commit()

    print("Menu items and ingredients added.\n")


# Add a test customer
def add_customer(session):
    print("Adding a customer to the database...")
    customer = CustomerPersonalInformation(
        address=123,
        birthday=datetime.now() - timedelta(days=365 * 30),  # 30 years ago
        phone_number=9876543210,
        gender="Male",
        previous_orders=2,
        age=30
    )
    session.add(customer)
    session.commit()
    print(f"Customer added with ID: {customer.id}\n")
    return customer.id


# Create an order and add sub-orders using OrderContainer
def create_order_with_suborders(session, customer_id):
    print(f"Creating order for customer ID: {customer_id}...")
    order_container = OrderContainer(session=session, customer_id=customer_id)

    # Add sub-orders
    print("Adding a sub-order for Margherita pizza...")
    order_container.add_suborder(menu_id=1,
                                 ingredient_ids=[1, 2])  # Assume Margherita (ID 1) and ingredients (Cheese, Tomato)

    print("Adding a sub-order for Coke drink...")
    order_container.add_suborder(menu_id=2)  # Assume Coke (ID 2), no ingredients needed

    # Finalize and display order
    session.commit()
    print(f"Order for customer ID {customer_id} has been created.\n")


# Display the created order details
def display_order_details(session, customer_id):
    print(f"Fetching order details for customer ID: {customer_id}...")

    orders = session.query(CustomerOrders).filter_by(customer_id=customer_id).all()
    for order in orders:
        print(
            f"Order ID: {order.id}, Status: {order.status}, Total Cost: {order.total_cost}, Ordered At: {order.ordered_at}")

    sub_orders = session.query(SubOrder).filter_by(order_id=orders[0].id).all()
    for sub_order in sub_orders:
        print(f"SubOrder ID: {sub_order.id}, Menu Item ID: {sub_order.item_id}")

    print("Order details displayed.\n")


# Main execution
if __name__ == "__main__":
    session = setup_database()

    # Add test data (menu items, ingredients, and customer)
    add_menu_items_and_ingredients(session)
    customer_id = add_customer(session)

    # Create an order and add sub-orders for that customer
    create_order_with_suborders(session, customer_id)

    # Display the order and sub-order details
    display_order_details(session, customer_id)

    # Close the session
    session.close()
