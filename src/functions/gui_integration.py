from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import cast, String

from src.tables.database import *


# gets drink/dessert, or returns all ingredients associated with the pizza
def get_menu_items_by_starting_id(session: Session, id: int):
    # Query all menu items whose id starts with the given value (id)
    menu_items = session.query(Menu).filter(cast(Menu.id, String).like(f'{id}%')).all()

    return menu_items


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
