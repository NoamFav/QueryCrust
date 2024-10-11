# routes/customer_routes.py
from flask import Blueprint, jsonify, request, session
from models.database import Menu, CustomerOrders, CustomerPersonalInformation, SubOrder, Ingredient, OrderedIngredient, Cart, CartItem, DeliveryDriver, Delivery
from datetime import datetime
from models import db
import traceback
import bcrypt
from sqlalchemy import func
from datetime import timedelta

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email').strip()
    password = data.get('password').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check if the user exists
    user = CustomerPersonalInformation.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Convert the hashed password back to bytes (it might be stored as a string)
    hashed_password = user.password.encode('utf-8') if isinstance(user.password, str) else user.password

    # Check if the password matches the hashed password
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return jsonify({'error': 'Invalid password'}), 401

    # Save user info in session
    session['user_id'] = user.id

    # Set cart info
    if user.cart:
        session['cart_id'] = user.cart.id
    else:
        cart = Cart(customer_id=user.id)
        db.session.add(cart)
        db.session.commit()
        session['cart_id'] = cart.id

    # Return user admin status along with other details
    return jsonify({
        'message': 'Login successful', 
        'user_id': user.id, 
        'cart_id': session['cart_id'], 
        'is_admin': user.is_admin
    })

@customer_bp.route('/signin', methods=['POST'])
def register():
    data = request.get_json()
    address = data.get('address')
    phone_number = data.get('phone_number')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    birthday = data.get('birthday')
    age = data.get('age')
    gender = data.get('gender')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    if not address or not phone_number or not name or not email or not birthday or not age or not gender or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    new_user = CustomerPersonalInformation(
        address=address,
        phone_number=phone_number,
        name=name,
        email=email,
        birthday=birthday,
        age=age,
        gender=gender,
        previous_orders=0,
        password=hashed_password  # Store the hashed password
    )
    db.session.add(new_user)
    db.session.commit()

    # Create a cart for the new user
    cart = Cart(customer_id=new_user.id)
    db.session.add(cart)
    db.session.commit()

    # Store the user and cart in the session
    session['user_id'] = new_user.id
    session['cart_id'] = cart.id

    # Create Delivery Driver at his position (postal code) if not exists already (its a dummy data and MAFIA PIZZA is not responsible for any delivery, its just MAGIC)
    driver = DeliveryDriver.query.filter_by(delivery_area=new_user.address).first()
    if not driver:
        driver = DeliveryDriver(delivery_area=new_user.address)
        db.session.add(driver)
        db.session.commit()
        print(f"New driver created for delivery area: {new_user.address}")

    return jsonify({
    'message': 'User created successfully',
    'user_id': new_user.id,
    'address': address,
    'phone_number': phone_number,
    'name': name,
    'email': email,
    'birthday': birthday,
    'age': age,
    'gender': gender,
    'previous_orders': 0,
    'password': password
    }), 201

@customer_bp.route('/details', methods=['GET'])
def get_customer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    user = CustomerPersonalInformation.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.id,
        'address': user.address,
        'phone_number': user.phone_number,
        'name': user.name,
        'email': user.email,
        'birthday': user.birthday,
        'gender': user.gender,
        })

@customer_bp.route('/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    if category:
        items = Menu.query.filter_by(category=category.lower()).all()
    else:
        items = Menu.query.all()
    menu = [{'id': item.id, 'name': item.name, 'price': item.price, 'category': item.category} for item in items]
    return jsonify(menu)

@customer_bp.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = Menu.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'category': item.category
    })

@customer_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    ingredient_list = [{'id': ingr.id, 'name': ingr.name, 'price': ingr.price} for ingr in ingredients]
    return jsonify(ingredient_list)

@customer_bp.route('/order', methods=['POST'])
def place_order():
    try:
        user_id = session.get('user_id')
        data = request.get_json()

        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401

        # Get user's cart
        cart = Cart.query.filter_by(customer_id=user_id).first()

        if not cart or not cart.items:
            return jsonify({'error': 'Cart is empty'}), 400

        # Calculate total cost of the order (for all items)
        total_cost = sum(item.total_price * item.quantity for item in cart.items)

        # Create a new customer order
        new_order = CustomerOrders(
            customer_id=user_id,
            total_cost=total_cost,
            ordered_at=datetime.now(),
            status='Pending',
            delivery_eta=None,  # Will be updated later
            address=data.get('address')  # Use the provided address
        )

        db.session.add(new_order)
        db.session.flush()  # Get the order.id

        # Track pizza and order count for each driver
        drivers_info = {}

        def find_or_create_driver(new_order, batch_pizza_count):
            """Find or create a driver for this order, ensuring limits are respected."""
            for driver_id, info in drivers_info.items():
                if info['pizza_count'] + batch_pizza_count <= 3 and info['order_count'] < 5:
                    return driver_id, info

            # No existing driver can take the batch, find a new driver
            driver = (
                DeliveryDriver.query
                .outerjoin(Delivery)
                .filter(DeliveryDriver.delivery_area == new_order.address)
                .group_by(DeliveryDriver.id)
                .having(func.count(Delivery.id) < 5)  # Max 5 orders per driver
                .order_by(func.count(Delivery.id))
                .first()
            )

            if not driver:
                # Create a new driver if none exist in the area
                driver = DeliveryDriver(delivery_area=new_order.address)
                db.session.add(driver)
                db.session.commit()

            # Initialize tracking for this driver
            drivers_info[driver.id] = {
                'pizza_count': 0,
                'order_count': 0
            }
            return driver.id, drivers_info[driver.id]

        # Process all cart items
        total_pizzas = sum(cart_item.quantity for cart_item in cart.items if cart_item.menu_item and cart_item.menu_item.category == 'pizza')

        # Create deliveries, respecting pizza and order limits
        for cart_item in cart.items:
            menu_item = cart_item.menu_item
            if not menu_item:
                continue  # Skip items with missing menu item references

            is_pizza = menu_item.category == 'pizza'
            batch_pizza_count = cart_item.quantity if is_pizza else 0

            # Find or create a driver for this batch
            driver_id, driver_info = find_or_create_driver(new_order, batch_pizza_count)

            # Create or add to a delivery
            delivery = Delivery(
                delivered_by=driver_id,
                order_id=new_order.id,
                assigned_at=datetime.now(),
                pizza_count=batch_pizza_count  # Assign pizza count to the delivery
            )

            # Update driver tracking information
            driver_info['pizza_count'] += batch_pizza_count
            driver_info['order_count'] += 1
            db.session.add(delivery)

            # Create sub-orders (directly handle quantities)
            sub_order = SubOrder(
                order_id=new_order.id,
                item_id=cart_item.menu_id,
                quantity=cart_item.quantity  # Handle quantities directly
            )
            db.session.add(sub_order)

        # Clear the user's cart after order creation
        for item in cart.items:
            db.session.delete(item)

        # Commit the transaction
        db.session.commit()

        # Fetch the deliveries to return the correct driver IDs
        deliveries = Delivery.query.filter_by(order_id=new_order.id).all()
        driver_ids = [delivery.delivered_by for delivery in deliveries]

        # Return the order details, including all drivers used for the order
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'total_cost': new_order.total_cost,
            'ordered_at': new_order.ordered_at.strftime('%d/%m/%Y %H:%M'),
            'delivery_drivers': driver_ids,  # List of drivers used for the order
            'address': new_order.address
        }), 201

    except Exception as e:
        print(f"Error placing order: {e}")
        db.session.rollback()  # Rollback the session on error
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/orders', methods=['GET'])
def get_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    orders = CustomerOrders.query.filter_by(customer_id=user_id).all()
    orders.sort(key=lambda x: x.ordered_at, reverse=True)

    for order in orders:
        if order.status == 'Pending':
            time_diff = datetime.now() - order.ordered_at
            if time_diff.total_seconds() >= 300:
                order.status = 'Cancelled'
                db.session.commit()

    order_list = []
    for order in orders:
        # Get all the drivers associated with the order
        deliveries = Delivery.query.filter_by(order_id=order.id).all()
        driver_ids = [delivery.delivered_by for delivery in deliveries]

        order_list.append({
            'order_id': order.id,
            'total_cost': order.total_cost,
            'ordered_at': order.ordered_at.strftime('%d/%m/%Y %H:%M'),
            'delivery_eta': order.delivery_eta.strftime('%d/%m/%Y %H:%M') if order.delivery_eta else None,
            'address': order.address,
            'status': order.status,
            'delivery_drivers': driver_ids  # Now returns multiple drivers if applicable
        })

    return jsonify(order_list)

@customer_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    order = CustomerOrders.query.get_or_404(order_id)
    sub_orders = SubOrder.query.filter_by(order_id=order_id).all()
    
    # Get all deliveries for this order
    deliveries = Delivery.query.filter_by(order_id=order_id).all()
    driver_ids = [delivery.delivered_by for delivery in deliveries]

    order_items = [
        {
            'id': sub_order.menu_item.id,
            'name': sub_order.menu_item.name,
            'price': sub_order.menu_item.price,
            'quantity': sub_order.quantity
        }
        for sub_order in sub_orders
    ]

    return jsonify({
        'order_id': order.id,
        'total_cost': order.total_cost,
        'ordered_at': order.ordered_at.strftime('%d/%m/%Y %H:%M'),
        'delivery_eta': order.delivery_eta.strftime('%d/%m/%Y %H:%M') if order.delivery_eta else None,
        'status': order.status,
        'items': order_items,
        'delivery_drivers': driver_ids  # List of drivers for the order
    })

@customer_bp.route('/orders/<int:order_id>/cancel', methods=['DELETE'])
def cancel_order(order_id):
    try:
        order = CustomerOrders.query.get_or_404(order_id)

        # If the order is 'Pending' and was placed less than 5 minutes ago, allow cancellation
        if order.status == 'Pending':
            time_diff = datetime.now() - order.ordered_at
            if time_diff.total_seconds() < 300: 
                # First delete any related delivery records
                Delivery.query.filter_by(order_id=order.id).delete()
                
                order.status = 'Cancelled'
                db.session.commit()
                return jsonify({'message': 'Order cancelled successfully'}), 200
            else:
                return jsonify({'error': 'Order cannot be cancelled after 5 minutes'}), 400

        # If the order is 'In Delivery', it cannot be cancelled
        if order.status == 'In Delivery':
            return jsonify({'error': 'Order is in delivery and cannot be cancelled'}), 400

        # If the order is 'Delivered' or 'Cancelled', allow deletion
        if order.status == 'Delivered' or order.status == 'Cancelled':
            # Delete any associated delivery records first
            Delivery.query.filter_by(order_id=order.id).delete()
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': 'Order has been removed successfully'}), 200

        # Otherwise, if the status is anything else, cancellation is not allowed
        return jsonify({'error': 'Order cannot be cancelled'}), 400
    except Exception as e:
        print(f"Error cancelling order: {e}")  # Log the error for debugging
        db.session.rollback()  # Roll back the session on error
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/cart', methods=['GET'])
def get_cart():
    print(f"Session data at cart fetch: {dict(session)}")  # Log session data
    cart = get_or_create_cart()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_items = [
        {
            'id': item.id,
            'menu_id': item.menu_id,
            'name': item.menu_item.name,
            'price': item.menu_item.price,
            'quantity': item.quantity,
            'customizations': item.customizations if item.customizations else [],
            'total_price': item.total_price * item.quantity
        }
        for item in cart.items
    ]
    return jsonify(cart_items)

@customer_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    print("Session data at cart add:", dict(session))  # Debug line
    try:
        data = request.get_json()
        menu_id = data.get('menu_id')
        quantity = data.get('quantity', 1)
        customizations = data.get('customizations', [])

        print(f"Received menu_id: {menu_id} (type: {type(menu_id)})")
        print(f"Received quantity: {quantity} (type: {type(quantity)})")
        print(f"Received customizations: {customizations} (type: {type(customizations)})")

        if not menu_id:
            return jsonify({'error': 'Menu ID is required'}), 400

        menu_item = Menu.query.get(menu_id)
        if not menu_item:
            return jsonify({'error': 'Menu item not found'}), 404

        cart = get_or_create_cart()
        assert cart, 'Cart not found'

        # Check if item already exists in cart
        cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_id=menu_id).first()
        if cart_item:
            cart_item.customizations = customizations
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                menu_id=menu_id,
                quantity=quantity,
                customizations=customizations if isinstance(customizations, list) else [],
                total_price=menu_item.price * quantity + sum(customization.get('price',0) for customization in customizations)
            )
            db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart'}), 200

    except Exception as e:
        # Log the error with traceback
        print("Error in /cart/add:", e)
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    if not cart_item_id:
        return jsonify({'error': 'Cart item ID is required'}), 400

    cart_item = CartItem.query.get(cart_item_id)
    if not cart_item:
        return jsonify({'error': 'Cart item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'})

def get_or_create_cart():
    user_id = session.get('user_id')
    
    if not user_id:
        print("No user_id found in session")
        return None

    print(f"Retrieving cart for user_id: {user_id}")
    cart = Cart.query.filter_by(customer_id=user_id).first()

    if cart:
        print(f"Cart found for user_id {user_id}: {cart.id}")
        session['cart_id'] = cart.id
        return cart
    else:
        print(f"No cart found for user_id {user_id}, creating a new cart.")
        try:
            cart = Cart(customer_id=user_id)
            db.session.add(cart)
            db.session.commit()
            session['cart_id'] = cart.id
            print(f"New cart created for user_id {user_id}")
            return cart
        except Exception as e:
            print(f"Error creating a new cart for user_id {user_id}: {e}")
            return None
