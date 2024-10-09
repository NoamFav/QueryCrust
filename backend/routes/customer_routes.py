# routes/customer_routes.py
from flask import Blueprint, jsonify, request, session
from models.database import Menu, CustomerOrders, CustomerPersonalInformation, SubOrder, OrderedIngredient, Ingredient, Cart, CartItem
from datetime import datetime
from models import db
import traceback
import bcrypt

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

    return jsonify({'message': 'Login successful', 'user_id': user.id})

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
    data = request.get_json()
    print(data)
    customer_info = data.get('customer_info')
    items = data.get('items')

    if not customer_info or not items:
        return jsonify({'error': 'Missing customer info or items'}), 400

    # Extract customer details
    address = customer_info.get('address')
    phone_number = customer_info.get('phone_number')
    name = customer_info.get('name')
    email = customer_info.get('email')
    birthday = customer_info.get('birthday')
    age = customer_info.get('age')
    gender = customer_info.get('gender')

    # Create a new customer record
    customer = CustomerPersonalInformation(
        address=address,
        phone_number=phone_number,
        name=name,
        birthday=birthday,
        email=email,
        gender=gender,
        previous_orders=0,
        age=age
    )
    db.session.add(customer)
    db.session.flush()  # Get customer.id

    # Create a new customer order
    order = CustomerOrders(
        customer_id=customer.id,
        total_cost=0,  # TODO: Update total cost
        ordered_at=datetime.now(),
        status='Pending',
        delivery_eta=None # TODO: Update delivery ETA
    )
    db.session.add(order)
    db.session.flush()  # Get order.id

    total_cost = 0

    # Process each item
    for item in items:
        menu_item_id = item.get('menu_item_id')
        quantity = item.get('quantity', 1) # TODO: Handle quantity
        customizations = item.get('customizations', [])  # List of ingredient IDs to add or remove

        menu_item = Menu.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item with id {menu_item_id} not found'}), 404

        # Create a sub-order for each item
        sub_order = SubOrder(
            order_id=order.id,
            item_id=menu_item.id,
        )
        db.session.add(sub_order * quantity)
        db.session.flush()  # Get sub_order.id

        # Handle customizations
        for customization in customizations:
            ingredient_id = customization.get('ingredient_id')
            action = customization.get('action')  # 'add' or 'remove'

            ingredient = Ingredient.query.get(ingredient_id)
            if not ingredient:
                return jsonify({'error': f'Ingredient with id {ingredient_id} not found'}), 404

            ordered_ingredient = OrderedIngredient(
                sub_order_id=sub_order.id,
                ingredient_id=ingredient.id,
                action=action
            )
            db.session.add(ordered_ingredient)

            # Update total cost based on customizations
            if action == 'add':
                total_cost += ingredient.price * quantity
            elif action == 'remove':
                total_cost -= ingredient.price * quantity

        # Update total cost for the menu item
        total_cost += menu_item.price * quantity

    # Update the order's total cost
    order.total_cost = total_cost

    db.session.commit()

    return jsonify({'message': 'Order placed successfully', 'order_id': order.id}), 201

@customer_bp.route('/cart', methods=['GET'])
def get_cart():
    cart = get_or_create_cart()
    cart_items = [
        {
            'id': item.id,
            'menu_id': item.menu_id,
            'name': item.menu_item.name,
            'price': item.menu_item.price,
            'quantity': item.quantity,
            'customizations': item.customizations if item.customizations else [],
            'total_price': item.menu_item.price * item.quantity
        }
        for item in cart.items
    ]
    return jsonify(cart_items)

@customer_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
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

        # Check if item already exists in cart
        cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_id=menu_id).first()
        if cart_item:
            cart_item.customizations = customizations   
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                menu_id=menu_id,
                quantity=quantity,
                customizations=customizations if isinstance(customizations, list) else []
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
    cart_id = session.get('cart_id')
    if cart_id:
        cart = Cart.query.get(cart_id)
        if cart:
            return cart
    # Create a new cart
    cart = Cart()
    db.session.add(cart)
    db.session.commit()
    session['cart_id'] = cart.id
    return cart
