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
        address="123",
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

def assign_order_driver(session, order_id):
    # Retrieve the order and customer details
    order = session.query(CustomerOrders).filter_by(id=order_id).first()
    if not order:
        print(f"Order with ID {order_id} not found.")
        return None

    customer = session.query(CustomerPersonalInformation).filter_by(id=order.customer_id).first()
    if not customer:
        print(f"Customer with ID {order.customer_id} not found.")
        return None

    postal_code = customer.address 
    print(f"Customer's postal code: {postal_code}")

    # Check for recent delivery in the same postal code
    current_time = datetime.now().replace(microsecond=0)  # Remove microseconds
    print(f"Current time: {current_time}")
    
    recent_delivery = session.query(Delivery).join(DeliveryDriver).filter(
        DeliveryDriver.delivery_area == postal_code,
        Delivery.pizza_count < 3,
        current_time - Delivery.assigned_at <= timedelta(minutes=3)
    ).first()

    if recent_delivery:
        # Add order to the existing delivery batch
        recent_delivery.pizza_count += 1
        session.commit()
        print(f"Order {order_id} added to the existing delivery batch handled by driver {recent_delivery.delivered_by}.")
        return recent_delivery.delivered_by

    # Fetch the available driver without microsecond logic in the query
    available_driver = session.query(DeliveryDriver).filter(
        DeliveryDriver.delivery_area == postal_code
    ).first()

    if available_driver:
        # Now handle the time difference calculation in Python
        driver_last_delivery = available_driver.last_delivery.replace(microsecond=0)
        time_difference = current_time - driver_last_delivery

        print(f"Found available driver: {available_driver.id}")
        print(f"Driver last delivery time: {driver_last_delivery}")
        print(f"Time difference: {time_difference}")

        if time_difference >= timedelta(minutes=15):
            available_driver.last_delivery = current_time

            delivery = Delivery(
                delivered_by=available_driver.id,
                order_id=order_id,
                pizza_count=1,
                assigned_at=current_time
            )

            session.add(delivery)
            session.commit()

            print(f"Order {order_id} assigned to driver {available_driver.id}.")
            return available_driver
        else:
            print(f"Driver {available_driver.id} is not yet available. Please try again later.")
            return None
    else:
        # Debug: Display available drivers
        drivers = session.query(DeliveryDriver).all()
        print(f"Available drivers: {drivers}")
        for driver in drivers:
            print(f"Driver ID: {driver.id}, Delivery Area: {driver.delivery_area}, Last Delivery: {driver.last_delivery}")
            print(f"Time difference with current_time: {current_time - driver.last_delivery.replace(microsecond=0)}")
        
        print(f"No available drivers for postal code {postal_code}. Please try again later.")
        return None

def add_test_driver(session):
    driver = DeliveryDriver(
        delivery_area="123",
        last_delivery=datetime.now() - timedelta(minutes=31)
    )
    session.add(driver)
    session.commit()
    print(f"Test driver added with ID: {driver.id}")


def test_multiple_orders_single_driver(session, customer_id):
    print("Testing multiple orders with a single driver...")
    
    # Create a second order for the same customer
    order_container_2 = OrderContainer(session=session, customer_id=customer_id)
    order_container_2.add_suborder(menu_id=1)  # Assume Margherita pizza again
    order_container_2.finalize_order()
    
    # Retrieve both orders
    orders = session.query(CustomerOrders).filter_by(customer_id=customer_id).all()
    print(f"Total orders created for customer: {len(orders)}")

    # Assign the driver to the first order
    driver = assign_order_driver(session, orders[0].id)
    assert driver is not None, "Driver was not assigned to the first order."

    # Now try assigning the same driver to the second order
    driver_2 = assign_order_driver(session, orders[1].id)
    assert driver_2 is not None, "Driver was not assigned to the second order."
    print("Single driver was assigned to handle multiple orders successfully.")

def test_no_available_drivers(session, customer_id):
    print("Testing driver unavailability...")

    # Set last delivery to be recent (within 15 minutes) to simulate unavailability
    driver = session.query(DeliveryDriver).first()
    driver.last_delivery = datetime.now()
    session.commit()
    
    # Create a new order
    order_container = OrderContainer(session=session, customer_id=customer_id)
    order_container.add_suborder(menu_id=1)  # Assume Margherita pizza again
    order_container.finalize_order()
    
    # Attempt to assign a driver to the new order
    order = session.query(CustomerOrders).filter_by(customer_id=customer_id).order_by(CustomerOrders.id.desc()).first()
    assigned_driver = assign_order_driver(session, order.id)
    
    assert assigned_driver is None, "Driver was incorrectly assigned when none should be available."
    print("Correctly handled the case where no drivers were available.")

# Main execution
if __name__ == "__main__":
    session = setup_database()

    # 1. Test Adding Menu Items and Ingredients
    add_menu_items_and_ingredients(session)
    
    # Validate menu items
    menu_items = session.query(Menu).all()
    assert len(menu_items) == 2, "Menu items were not added correctly."
    print("Menu items added successfully.")
    
    # 2. Test Adding a Customer
    customer_id = add_customer(session)
    
    # Validate the customer
    customer = session.query(CustomerPersonalInformation).filter_by(id=customer_id).first()
    assert customer is not None, "Customer was not added correctly."
    print("Customer added successfully.")
    
    # 3. Test Creating an Order with Sub-Orders
    create_order_with_suborders(session, customer_id)
    
    # Validate the order and sub-orders
    orders = session.query(CustomerOrders).filter_by(customer_id=customer_id).all()
    assert len(orders) > 0, "Order was not created correctly."
    print("Order created successfully.")
    
    sub_orders = session.query(SubOrder).filter_by(order_id=orders[0].id).all()
    assert len(sub_orders) == 2, "Sub-orders were not added correctly."
    print("Sub-orders added successfully.")
    
    # 4. Test Displaying Order Details
    display_order_details(session, customer_id)

    # Add a test driver
    add_test_driver(session)

    # 5. Test Assigning a Delivery Driver
    driver = assign_order_driver(session, orders[0].id)
    
    assert driver is not None, "Driver was not assigned correctly."
    print(f"Order {orders[0].id} was assigned to driver {driver.id}.")

    # additional tests
    test_multiple_orders_single_driver(session, customer_id)
    test_no_available_drivers(session, customer_id)
    
    # Close the session
    session.close()
