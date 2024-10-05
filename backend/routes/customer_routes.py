from flask import Blueprint, jsonify, request
from models.database import Menu, CustomerOrders, CustomerPersonalInformation, SubOrder, OrderedIngredient, Ingredient
from datetime import datetime
from app import db

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/menu', methods=['GET'])
def get_menu():
    items = Menu.query.all()
    menu = [{'id': item.id, 'name': item.name, 'price': item.price, 'category': item.category} for item in items]
    return jsonify(menu)

@customer_bp.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
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
