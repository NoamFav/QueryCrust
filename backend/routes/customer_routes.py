# routes/customer_routes.py
from flask import Blueprint, jsonify, request, session
from models.database import (
    Menu,
    CustomerOrders,
    CustomerPersonalInformation,
    SubOrder,
    Ingredient,
    OrderedIngredient,
    Cart,
    CartItem,
    DeliveryDriver,
    Delivery,
    Discounts,
    PizzaIngredient,
)
from datetime import datetime
from models import db
import traceback
import bcrypt
from sqlalchemy import func
from datetime import timedelta
from sqlalchemy import or_

customer_bp = Blueprint("customer_bp", __name__)


@customer_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email").strip()
    password = data.get("password").strip()

    # Check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user exists
    user = CustomerPersonalInformation.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Create hashed password
    hashed_password = (
        user.password.encode("utf-8")
        if isinstance(user.password, str)
        else user.password
    )

    # Check if password is correct with bcrypt
    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return jsonify({"error": "Invalid password"}), 401

    # Set session variables
    session["user_id"] = user.id

    # Check if user has a cart
    if user.cart:
        session["cart_id"] = user.cart.id
    else:
        # If user does not have a cart, create a new cart
        cart = Cart(customer_id=user.id)
        db.session.add(cart)
        db.session.commit()
        session["cart_id"] = cart.id

    # Return user information to frontend
    return jsonify(
        {
            "message": "Login successful",
            "user_id": user.id,
            "cart_id": session["cart_id"],
            "is_admin": user.is_admin,
        }
    )


# Register a new user
@customer_bp.route("/signin", methods=["POST"])
def register():
    # Get user data from request
    data = request.get_json()
    address = data.get("address")
    phone_number = data.get("phone_number")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")
    birthday = data.get("birthday")
    age = data.get("age")
    gender = data.get("gender")

    # Hash the password with bcrypt for security
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Check if all required fields are provided
    if (
        not address
        or not phone_number
        or not name
        or not email
        or not birthday
        or not age
        or not gender
        or not password
    ):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new user with the provided data
    new_user = CustomerPersonalInformation(
        address=address,
        phone_number=phone_number,
        name=name,
        email=email,
        birthday=birthday,
        age=age,
        gender=gender,
        previous_orders=0,
        password=hashed_password,
    )
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Create a new cart for the user
    cart = Cart(customer_id=new_user.id)
    db.session.add(cart)
    db.session.commit()

    # Set session variables
    session["user_id"] = new_user.id
    session["cart_id"] = cart.id

    # Check if a delivery driver exists for the user's address
    # Pure magic, don't worry about it, its not entirely black magic and more or less painless (I hope)
    driver = DeliveryDriver.query.filter_by(delivery_area=new_user.address).first()
    if not driver:
        driver = DeliveryDriver(delivery_area=new_user.address)
        db.session.add(driver)
        db.session.commit()
        print(
            f"A new driver appeared from thin air for delivery area: {new_user.address}"
        )  # I'm not crazy, you're crazy

    # Return user information to frontend
    return (
        jsonify(
            {
                "message": "User created successfully",
                "user_id": new_user.id,
                "address": address,
                "phone_number": phone_number,
                "name": name,
                "email": email,
                "birthday": birthday,
                "age": age,
                "gender": gender,
                "previous_orders": 0,
                "password": password,
            }
        ),
        201,
    )


# Get user information
@customer_bp.route("/details", methods=["GET"])
def get_customer():
    # Check if user is authenticated
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Get user information from the database
    user = CustomerPersonalInformation.query.get_or_404(user_id)
    return jsonify(
        {
            "user_id": user.id,
            "address": user.address,
            "phone_number": user.phone_number,
            "name": user.name,
            "email": user.email,
            "birthday": user.birthday,
            "gender": user.gender,
            "previous_orders": user.previous_orders,
            "last_order": (
                user.last_order.strftime("%Y-%m-%d %H:%M:%S")
                if user.last_order
                else None
            ),
        }
    )


# Get menu items
@customer_bp.route("/menu", methods=["GET"])
def get_menu():

    # Get categories from the menu
    category = request.args.get("category")

    # Get menu items from the database if category is provided
    if category:
        items = Menu.query.filter_by(
            category=category.lower()
        ).all()  # Filter by category
    else:
        items = Menu.query.all()  # Get all menu items

    # Create a list of menu items to return
    menu = [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "category": item.category,
        }
        for item in items
    ]
    for menu_item in menu:
        if menu_item["category"] == "pizza":
            pizza_ingredients = PizzaIngredient.query.filter_by(
                menu_id=menu_item["id"]
            ).all()
            menu_item["ingredients"] = [
                {"name": ingredient.ingredient.name} for ingredient in pizza_ingredients
            ]

            is_vegan = all(
                ingredient.ingredient.is_vegan for ingredient in pizza_ingredients
            )
            is_vegetarian = all(
                ingredient.ingredient.is_vegetarian for ingredient in pizza_ingredients
            )
            menu_item["is_vegan"] = is_vegan
            menu_item["is_vegetarian"] = is_vegetarian

    return jsonify(menu)


# Get a single menu item
@customer_bp.route("/menu/<int:item_id>", methods=["GET"])
def get_menu_item(item_id):
    # Get a single menu item from the database with its ID
    item = Menu.query.get_or_404(item_id)
    return jsonify(
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "category": item.category,
        }
    )


# Get ingredients
@customer_bp.route("/ingredients", methods=["GET"])
def get_ingredients():
    # Get all ingredients from the database
    ingredients = Ingredient.query.all()

    # Create a list of ingredients to return
    ingredient_list = [
        {
            "id": ingr.id,
            "name": ingr.name,
            "price": ingr.price,
            "is_vegan": ingr.is_vegan,
            "is_vegetarian": ingr.is_vegetarian,
        }
        for ingr in ingredients
    ]
    return jsonify(ingredient_list)


# Reset pizza counts for all drivers with active orders
def reset_pizza_counts():

    # Get all delivery drivers
    drivers = DeliveryDriver.query.all()
    for driver in drivers:

        # Get all active deliveries for the driver
        active_deliveries = (
            Delivery.query.filter_by(delivered_by=driver.id)
            .join(CustomerOrders)
            .filter(CustomerOrders.status != "Delivered")
            .all()
        )

        # Calculate the total number of pizzas assigned to the driver with the active orders
        total_pizzas = sum(delivery.pizza_count for delivery in active_deliveries)

        print(
            f"Driver {driver.id} has {total_pizzas} pizzas assigned in active orders."
        )


@customer_bp.route("/discount", methods=["POST"])
def apply_discount():

    data = request.get_json()
    discount_code = data.get("discount_code")

    discounts = Discounts.query.all()
    discount_codes = [discount.name for discount in discounts]

    if discount_code not in discount_codes:
        return jsonify({"error": "Invalid discount code"}), 400

    discount = Discounts.query.filter_by(name=discount_code).first()
    assert discount, "Discount not found"

    if discount.used:
        return jsonify({"error": "Discount code has already been used"}), 400

    return (
        jsonify(
            {
                "message": "Discount code applied successfully",
                "discount_name": discount.name,
                "discount_value": discount.value,
            }
        ),
        200,
    )


def apply_margin_and_VAT(price):
    # Apply a 40% margin to the price
    price = price * 1.40
    # Apply a 9% VAT to the price
    price = price * 1.09
    return price


# Place an order
@customer_bp.route("/order", methods=["POST"])
def place_order():
    try:
        # Get user ID from session to have its orders placed
        user_id = session.get("user_id")
        data = request.get_json()

        # Check if user is authenticated (should not happen)
        if not user_id:
            return jsonify({"error": "User not authenticated"}), 401

        # Reset pizza counts for all drivers with active orders
        reset_pizza_counts()

        # Get the user's cart
        cart = Cart.query.filter_by(customer_id=user_id).first()

        # Check if the cart is empty or does not exist
        if not cart or not cart.items:
            return jsonify({"error": "Cart is empty"}), 400

        # Calculate the total cost of the order with the items in the cart times their quantities
        total_cost = sum(item.total_price * item.quantity for item in cart.items)

        # Apply a 40% margin and 9% VAT to the total cost
        total_cost = apply_margin_and_VAT(total_cost)

        discount_code = data.get(
            "discountName"
        )  # Get the discount code from the request database
        if discount_code:
            discount = Discounts.query.filter_by(name=discount_code).first()
            assert discount, "Discount not found"
            discount.used = True  # Mark the discount as used

        discount = data.get(
            "discountValue"
        )  # Get the discount value from the request data
        if discount:
            total_cost = total_cost * (
                1 - discount
            )  # Apply the discount to the total cost
            total_cost = round(
                total_cost, 2
            )  # Round the total cost to 2 decimal places

        # Update the customer information with the new order
        customer_info = CustomerPersonalInformation.query.get(user_id)
        assert customer_info, "Customer not found"
        customer_info.previous_orders += (
            1  # Increase the number of previous orders for the customer
        )
        customer_info.last_order = (
            datetime.now()
        )  # Set the last order date and time to the current date and time

        if customer_info.previous_orders % 10 == 0:
            # If the customer has placed 10 orders, apply a 10% discount to the total cost (loyalty discount)
            total_cost = total_cost * 0.90

        if customer_info.birthday == datetime.now().date():
            pizza = Menu.query.filter_by(category="pizza").first()
            if pizza:
                total_cost = (
                    total_cost - pizza.price
                )  # Give the customer a free pizza on their birthday

        total_cost = round(total_cost, 2)  # Round the total cost to 2 decimal places

        # Create a new order with the user's ID, total cost, and address
        new_order = CustomerOrders(
            customer_id=user_id,
            total_cost=total_cost,
            ordered_at=datetime.now(),  # Get the current date and time
            status="Pending",  # Set the status of the order to pending, it will be updated by the admin as the order is processed
            delivery_eta=datetime.now()
            + timedelta(
                minutes=30
            ),  # Set the delivery ETA to 30 minutes from now (for testing purposes)
            address=data.get(
                "address"
            ),  # Get the address from the request data not from the user's information (You may need to deliver to a different address)
        )

        # Add the new order to the database
        db.session.add(new_order)
        db.session.flush()

        # Function to find or create a driver for the delivery area
        def find_or_create_driver(item_quantity=0):

            # Get a driver for the delivery area with the following conditions:
            # - The driver has less than 5 orders
            # - The driver has less than 3 pizzas assigned
            # - The driver has the most number of orders to create more batches (better for ease of delivery)
            driver = (
                DeliveryDriver.query.outerjoin(Delivery)
                .filter(
                    DeliveryDriver.delivery_area == new_order.address,
                    or_(
                        Delivery.assigned_at == None,
                        Delivery.assigned_at < datetime.now() - timedelta(minutes=30),
                    ),
                )  # Get drivers with no deliveries or deliveries older than 30 minutes
                .group_by(DeliveryDriver.id)
                .having(func.count(Delivery.id) < 5)  # Max 5 orders per driver
                .having(
                    or_(
                        func.sum(Delivery.pizza_count) + item_quantity <= 3,
                        func.sum(Delivery.pizza_count).is_(None),
                    )
                )  # Ensure total pizza count doesn't exceed 3 or isn't None (cause apparently None isn't inferior to 3)
                .order_by(
                    func.count(Delivery.id).desc()
                )  # Create more batches if possible
                .first()
            )

            if not driver:
                # If no drivers are available, create a new driver for the delivery area
                driver = DeliveryDriver(delivery_area=new_order.address)
                db.session.add(driver)
                db.session.commit()

            return driver

        # Initialize variables for the pizza count and driver information
        pizza_count = 0
        drivers_info = []
        delivery = None

        # Process each item in the cart
        for cart_item in cart.items:

            # Get the menu item for the cart item
            menu_item = cart_item.menu_item

            # Skip the item if it does not exist
            if not menu_item:
                continue

            # Check if the item is a pizza
            is_pizza = menu_item.category == "pizza"

            # Get the quantity of the item in the cart
            item_quantity = cart_item.quantity

            # Get the total number of pizzas in the cart
            # Its a bit of a hack, but it works
            # Could definitely be done better but I'm not sure how and don't want to break anything
            # Definitely didn't spend 2 hours trying to figure out how to do it better
            pizza_amount = 0
            for cart_item_pizza in cart.items:
                if cart_item_pizza.menu_item.category == "pizza":
                    pizza_amount += cart_item_pizza.quantity

            # Process the item in the cart based on the quantity
            while item_quantity > 0:

                # Calculate the remaining capacity for the driver
                remaining_capacity = 3 - pizza_count if is_pizza else 3

                # If the pizza count exceeds 3 or the delivery is None, find or create a driver for the delivery area
                if pizza_count > 3 or delivery is None:
                    driver = find_or_create_driver(pizza_amount)

                    # Create a new delivery for the driver with the order ID and the current date and time
                    delivery = Delivery(
                        delivered_by=driver.id,
                        order_id=new_order.id,
                        assigned_at=datetime.now(),
                        pizza_count=0,  # Start with 0 pizzas
                    )

                    # Add the delivery to the database
                    db.session.add(delivery)
                    drivers_info.append(delivery)
                    pizza_count = 0  # Reset the pizza count for the new delivery

                # If the item is a pizza, add it to the delivery
                if is_pizza:
                    # Calculate the number of pizzas to add to the delivery based on the remaining capacity and the quantity of the item
                    pizzas_to_add = min(item_quantity, remaining_capacity)
                    delivery.pizza_count += (
                        pizzas_to_add  # Increase the pizza count for the delivery
                    )
                    pizza_count += pizzas_to_add  # Increase the total pizza count
                    item_quantity -= pizzas_to_add  # Decrease the remaining pizzas
                else:
                    item_quantity = 0  # Process all non-pizza items in one step

                # Create a sub-order for the item in the cart
                sub_order = SubOrder(
                    order_id=new_order.id,
                    item_id=cart_item.menu_id,
                    quantity=cart_item.quantity,
                )

                # Add the sub-order to the database
                db.session.add(sub_order)
                db.session.flush()

                # Get the customizations for the item in the cart
                if cart_item.customizations:
                    # Process each customization for the item
                    for customization in cart_item.customizations:
                        # Create an ordered ingredient for the customization
                        ordered_ingredient = OrderedIngredient(
                            sub_order_id=sub_order.id,
                            ingredient_id=customization["ingredient_id"],
                            action=customization["action"],
                        )
                        # Add the ordered ingredient to the database
                        # Will be used to track the customizations for the item and compute the total cost
                        db.session.add(ordered_ingredient)

        # Delete the items in the cart after processing the order
        for item in cart.items:
            db.session.delete(item)

        # Commit the changes to the database
        db.session.commit()

        # Get the driver IDs for the delivery
        driver_ids = [delivery.delivered_by for delivery in drivers_info]

        # Return the order information to the frontend
        return (
            jsonify(
                {
                    "message": "Order placed successfully",
                    "order_id": new_order.id,
                    "total_cost": new_order.total_cost,
                    "ordered_at": new_order.ordered_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # Format the date and time as a string like 'YYYY-MM-DD HH:MM:SS'
                    "delivery_eta": new_order.delivery_eta.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # Format the delivery ETA as a string like 'YYYY-MM-DD HH:MM:SS'
                    "delivery_drivers": driver_ids,  # Get the driver IDs for the delivery (multiple drivers if the order has multiple batches)
                    "address": new_order.address,
                }
            ),
            201,
        )

    except Exception as e:
        # Handle any errors that occur during the order placement process
        print(f"Error placing order: {e}")
        # Rollback the changes to the database (transaction TADAAA)
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500


# Get all orders for the user
@customer_bp.route("/orders", methods=["GET"])
def get_order():
    # Get the user ID from the session to get the orders for the user
    user_id = session.get("user_id")
    # Check if the user is authenticated (should not happen)
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Get all orders for the user from the database
    orders = CustomerOrders.query.filter_by(customer_id=user_id).all()

    # Sort the orders by the ordered date and time in descending order to have the latest orders first
    orders.sort(key=lambda x: x.ordered_at, reverse=True)

    # Cancel orders that have been pending for more than 10 minutes
    # This makes sure that the orders are not stuck in the pending state meaning that the restaurant has not handled them
    # Also this is a good way to make sure that the orders are not stuck in the pending state
    for order in orders:
        if order.status == "Pending":
            # Calculate the time difference between the current date and time and the ordered date and time
            time_diff = datetime.now() - order.ordered_at
            if time_diff.total_seconds() >= 600:
                order.status = "Cancelled"  # Set the status of the order to cancelled (it could be expired but we don't want to confuse the user)
                db.session.commit()  # Commit the changes to the database

    # Create a list of orders to return
    order_list = []

    # Process each order to get the order information
    for order in orders:

        if order.status == "Delivered" or order.status == "Cancelled":
            continue  # Skip the order if it is delivered or cancelled (we don't need to show it to the user but we need to keep it in the database for records)

        # Get the sub-orders for the order based on the order ID
        deliveries = Delivery.query.filter_by(order_id=order.id).all()

        # Get the driver IDs for the delivery
        # Shown as a list of driver IDs for the order
        # But don't show the delivery itself, that would be too much information that the user doesn't need
        driver_ids = [delivery.delivered_by for delivery in deliveries]

        # Add the order information to the list
        order_list.append(
            {
                "order_id": order.id,
                "total_cost": order.total_cost,
                "ordered_at": order.ordered_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),  # Format the ordered date and time as a string like 'YYYY-MM-DD HH:MM:SS'
                "delivery_eta": order.delivery_eta.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),  # Format the delivery ETA as a string like 'YYYY-MM-DD HH:MM:SS'
                "address": order.address,
                "status": order.status,
                "delivery_drivers": driver_ids,  # Get the driver IDs for the delivery
            }
        )

    return jsonify(order_list)


# Get the details of a single order
@customer_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order_details(order_id):
    # Get the order details from the database based on the order ID
    order = CustomerOrders.query.get_or_404(order_id)

    # Get the sub-orders for the order based on the order ID
    sub_orders = SubOrder.query.filter_by(order_id=order_id).all()

    # Get the driver IDs for the delivery
    deliveries = Delivery.query.filter_by(order_id=order_id).all()

    # Get the driver IDs for the delivery
    driver_ids = [delivery.delivered_by for delivery in deliveries]

    # Create a JSON object with the order information
    order_items = [
        {
            "id": sub_order.menu_item.id,
            "name": sub_order.menu_item.name,
            "price": sub_order.menu_item.price,
            "quantity": sub_order.quantity,
        }
        for sub_order in sub_orders
    ]

    # Return the order information to the frontend
    return jsonify(
        {
            "order_id": order.id,
            "total_cost": order.total_cost,
            "ordered_at": order.ordered_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Format the ordered date and time as a string like 'YYYY-MM-DD HH:MM:SS'
            "delivery_eta": (
                order.delivery_eta.strftime("%Y-%m-%d %H:%M:%S")
                if order.delivery_eta
                else None
            ),  # Format the delivery ETA as a string like 'YYYY-MM-DD HH:MM:SS'
            "status": order.status,
            "items": order_items,  # Get the items for the order
            "delivery_drivers": driver_ids,  # Get the driver IDs for the delivery
        }
    )


# Get the details of a single order
@customer_bp.route("/orders/<int:order_id>/cancel", methods=["DELETE"])
def cancel_order(order_id):
    try:
        # Get the order details from the database based on the order ID
        order = CustomerOrders.query.get_or_404(order_id)

        # Check if the order can be cancelled
        if order.status == "Pending":
            # Calculate the time difference between the current date and time and the ordered date and time
            time_diff = datetime.now() - order.ordered_at
            # Check if the time difference is less than 5 minutes
            if time_diff.total_seconds() < 300:
                # If it is less than 5 minutes, mark the order as cancelled (delete it later)
                Delivery.query.filter_by(order_id=order.id).delete()

                # Mark the order as cancelled
                order.status = "Cancelled"
                db.session.commit()
                return jsonify({"message": "Order cancelled successfully"}), 200
            else:
                # If it is more than 5 minutes, return an error message
                return (
                    jsonify({"error": "Order cannot be cancelled after 5 minutes"}),
                    400,
                )

        # If the order is in delivery, you cannot cancel it (you can't cancel an order that is already on its way DUH)
        if order.status == "In Delivery":
            return (
                jsonify({"error": "Order is in delivery and cannot be cancelled"}),
                400,
            )

        # If the order is delivered or cancelled, you can remove it from the database
        if order.status == "Delivered" or order.status == "Cancelled":
            # temporarily commented out to prevent deletion of orders from the database for records

            # Get the sub-orders for the order based on the order ID
            # sub_orders = SubOrder.query.filter_by(order_id=order.id).all()

            # From the sub-orders, get the ordered ingredients for the order and delete them
            # for sub_order in sub_orders:
            # OrderedIngredient.query.filter_by(sub_order_id=sub_order.id).delete()

            # SubOrder.query.filter_by(order_id=order.id).delete() # Delete the sub-orders for the order
            # Delivery.query.filter_by(order_id=order.id).delete() # Delete the deliveries for the order
            # db.session.delete(order) # Delete the order
            # db.session.commit() # Commit the changes to the database
            return jsonify({"message": "Order has been removed successfully"}), 200

        return jsonify({"error": "Order cannot be cancelled"}), 400
    except Exception as e:
        # Handle any errors that occur during the order cancellation process
        print(f"Error cancelling order: {e}")
        db.session.rollback()  # Rollback the changes to the database (transaction)
        return jsonify({"error": "Internal Server Error"}), 500


# Get all delivery drivers
@customer_bp.route("/cart", methods=["GET"])
def get_cart():
    # Get the user ID from the session to get the cart for the user
    print(f"Session data at cart fetch: {dict(session)}")
    # Get the cart ID from the session to get the cart for the user
    cart = get_or_create_cart()

    # Check if the cart does not exist
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    # Get the items in the cart
    cart_items = [
        {
            "id": item.id,
            "menu_id": item.menu_id,
            "name": item.menu_item.name,
            "price": item.menu_item.price,
            "quantity": item.quantity,
            "customizations": (
                item.customizations if item.customizations else []
            ),  # Get the customizations for the item
            "total_price": item.total_price * item.quantity,
        }
        for item in cart.items  # Get the items in the cart
    ]
    return jsonify(cart_items)


# Add an item to the cart
@customer_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    print("Session data at cart add:", dict(session))

    try:
        # Get the data from the request to add an item to the cart
        data = request.get_json()
        menu_id = data.get("menu_id")
        quantity = data.get("quantity", 1)
        customizations = data.get("customizations", [])

        print(f"Received menu_id: {menu_id} (type: {type(menu_id)})")
        print(f"Received quantity: {quantity} (type: {type(quantity)})")
        print(
            f"Received customizations: {customizations} (type: {type(customizations)})"
        )

        # Check if the menu ID is provided
        if not menu_id:
            return jsonify({"error": "Menu ID is required"}), 400

        # Check if the quantity is provided
        menu_item = Menu.query.get(menu_id)
        if not menu_item:
            return jsonify({"error": "Menu item not found"}), 404

        # Get the cart for the user or create a new cart if it does not exist
        cart = get_or_create_cart()
        assert cart, "Cart not found"

        # Check if the item is already in the cart
        cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_id=menu_id).first()
        if cart_item and cart_item.customizations == customizations:
            # If the item is already in the cart, increase the quantity
            # It has to have the same customizations to be considered the same item
            cart_item.customizations = customizations
            cart_item.quantity += quantity
        else:
            # If the item is not in the cart, create a new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                menu_id=menu_id,
                quantity=quantity,
                customizations=(
                    customizations if isinstance(customizations, list) else []
                ),  # Set the customizations for the item
                total_price=menu_item.price * quantity
                + sum(
                    customization.get("price", 0) for customization in customizations
                ),
            )
            db.session.add(cart_item)  # Add the cart item to the database
        db.session.commit()  # Commit the changes to the database
        return jsonify({"message": "Item added to cart"}), 200

    except Exception as e:
        # Handle any errors that occur during the item addition process
        print("Error in /cart/add:", e)
        traceback.print_exc()  # Print the traceback for the error
        return jsonify({"error": "Internal Server Error"}), 500


# Remove an item from the cart
@customer_bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    # Get the data from the request to remove an item from
    data = request.get_json()

    # Check if the cart item ID is provided if not return an error
    cart_item_id = data.get("cart_item_id")
    if not cart_item_id:
        return jsonify({"error": "Cart item ID is required"}), 400

    # Get the cart item from the database based on the cart item ID if not return an error
    cart_item = CartItem.query.get(cart_item_id)
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    # Delete the cart item from the database
    db.session.delete(cart_item)

    # Commit the changes to the database
    db.session.commit()
    return jsonify({"message": "Item removed from cart"})


def get_or_create_cart():

    # Get the user ID from the session
    user_id = session.get("user_id")

    # Check if the user ID is not provided
    if not user_id:
        print("No user_id found in session")
        return None

    # Get the cart ID from the session
    print(f"Retrieving cart for user_id: {user_id}")
    cart = Cart.query.filter_by(customer_id=user_id).first()

    # Check if the cart exists
    if cart:
        # If the cart exists, return the cart
        print(f"Cart found for user_id {user_id}: {cart.id}")
        session["cart_id"] = cart.id
        return cart
    else:
        # If the cart does not exist, create a new cart
        print(f"No cart found for user_id {user_id}, creating a new cart.")
        try:
            cart = Cart(customer_id=user_id)
            db.session.add(cart)
            db.session.commit()
            session["cart_id"] = cart.id
            print(f"New cart created for user_id {user_id}")
            return cart
        except Exception as e:
            print(f"Error creating a new cart for user_id {user_id}: {e}")
            return None
