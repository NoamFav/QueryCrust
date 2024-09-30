from sqlalchemy import engine

from src.data.database import *
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class OrderContainer:
    def __init__(self, session: Session, customer_id: int):
        """
        Initialize the OrderContainer class with the session and customer ID.

        :param session: SQLAlchemy session.
        :param customer_id: ID of the customer placing the order.
        """
        self.session = session
        self.sub_orders = []  # so that we can keep track of all the parts of our customers order for the finall "1 pizza test"
        self.order = CustomerOrders(
            customer_id=customer_id,
            total_cost=0,  # Initialize with 0, we will update later
            delivery_eta=datetime.now(),  # will update later as well
            ordered_at=datetime.now(),
            status='pending'
        )
        self.session.add(self.order)
        self.session.flush()

    def add_suborder(self, menu_id: int, ingredient_ids=None):
        """
        Add a sub-order for the current order with a menu item and optional ingredients.

        :param menu_id: ID of the menu item being added.
        :param ingredient_ids: Optional list of ingredient IDs for the menu item.
        """
        if not self.order:
            raise ValueError("Order has not been created yet. Call create_order() first.")

        sub_order = SubOrder(
            item_id=menu_id,
            order_id=self.order.id
        )
        self.session.add(sub_order)
        self.sub_orders.append(sub_order)
        self.session.flush()

        # Fetch the menu item and calculate the price
        menu_item = self.session.query(Menu).filter_by(id=menu_id).first()
        assert menu_item, f"Menu item with ID {menu_id} not found."
        self.order.total_cost += menu_item.calculate_total_price(self.session)

        if ingredient_ids:
            for ingredient_id in ingredient_ids:
                ordered_pizza_ingredient = OrderedIngredient(
                    sub_order_id=sub_order.id,
                    ingredient_id=ingredient_id
                )
                self.session.add(ordered_pizza_ingredient)
                # Fetch the ingredient and calculate price with profit and VAT
                ingredient = self.session.query(Ingredient).filter_by(id=ingredient_id).first()
                ingredient_price = float(ingredient.price)
                price_with_profit = ingredient_price * 1.4
                final_price = price_with_profit * 1.09
                self.order.total_cost += round(final_price, 2)
        self.session.commit()
    
    def validate_pizza_in_order(self):
        """
        Validate that the order contains at least one pizza.
        Raises a ValueError if no pizza is found in the sub-orders.
        """
        has_pizza = False
        for sub_order in self.sub_orders:
            # Check if the sub_order's menu item belongs to the pizza category
            menu_item = self.session.query(Menu).filter_by(id=sub_order.item_id).first()
            if menu_item and menu_item.category == 'pizza':
                has_pizza = True
                break

        if not has_pizza:
            raise ValueError("The order must contain at least one pizza.")

    def finalize_order(self):
        """
        Finalize the order by committing the session.
        """
        if not self.order:
            raise ValueError("Order has not been created yet.")

        # adding a 25 minute delivery time arbitrarily
        self.order.delivery_eta = datetime.now() + timedelta(minutes=25)
        # Commit the session to save all the changes (customer order, sub-orders, ingredients)
        self.session.commit()
        print(f"Order {self.order.id} finalized with total cost: ${self.order.total_cost:.2f}")
