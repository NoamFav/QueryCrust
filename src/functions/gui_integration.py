from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from src.tables import pizza_ingredient_junction
from src.tables.customer_orders import CustomerOrders
from src.tables.menu import Menu
from src.tables.sub_order import SubOrder


# gets drink/dessert, or returns all ingredients associated with the pizza
def get_menu_item_by_starting_id(session: Session, id: int):

    menu_items = session.query(Menu).filter(cast(Menu.id, String).like(f'{id}%')).all()
    # Query the PizzaIngredient table to find all related ingredients for the menu_ids
    if id == 1:
        items = session.query(pizza_ingredient_junction).filter(pizza_ingredient_junction.menu_id.in_(menu_items)).all()
    else:
        items = session.query(Menu).filter(cast(Menu.id, String).like('1%')).all()

    return items


def get_non_completed_orders(session: Session):
    # Query to filter customer orders where the status is not 'completed'
    active_orders = session.query(CustomerOrders).filter(CustomerOrders.status != 'completed').all()
    return active_orders


def create_customer_order(session: Session, customer_id: int, menu_id: int, ingredients_ids=None):

    try:
        # Create a new customer order
        new_order = CustomerOrders(
            customer_id=customer_id,
            total_cost=0,  # Initialize with 0, we will update later
            delivery_eta=datetime.now(),  # You can adjust the ETA calculation as needed
            ordered_at=datetime.now(),
            status='pending'
        )
        session.add(new_order)
        session.flush()  # Flush to generate the new order's ID before creating sub-orders

        # Create a sub-order for the selected menu item
        sub_order = SubOrder(
            item_id=menu_id,
            order_id=new_order.id
        )
        session.add(sub_order)

        # Optionally handle ingredients (if any are provided)
        if ingredients_ids:
            for ingredient_id in ingredients_ids:
                pizza_ingredient = PizzaIngredient(
                    menu_id=menu_id,
                    ingredient_id=ingredient_id
                )
                session.add(pizza_ingredient)

        # Commit the transaction
        session.commit()

        # Return the created order for further processing
        return new_order

    except Exception as e:
        # In case of any error, rollback the transaction
        session.rollback()
        print(f"An error occurred while creating the order: {e}")
        return None