# routes/admin_routes.py
from flask import Blueprint, jsonify, request
from models.database import Menu, CustomerOrders, DeliveryDriver, OrderedIngredient, SubOrder, CartItem, Delivery
from models import db

admin_bp = Blueprint('admin_bp', __name__)

# Get all menu items
@admin_bp.route('/menu', methods=['GET'])
def get_menu():
    items = Menu.query.all()
    menu = [{'id': item.id, 'name': item.name, 'price': item.price, 'category': item.category} for item in items]
    return jsonify(menu)

@admin_bp.route('/orders', methods=['GET'])
def get_all_orders():
    orders = CustomerOrders.query.all()  # Fetch all orders
    order_list = []

    for order in orders:
        customer = order.customer  # Get the customer associated with the order
        
        # Get all deliveries for this order
        deliveries = Delivery.query.filter_by(order_id=order.id).all()
        driver_ids = [delivery.delivered_by for delivery in deliveries]

        order_info = {
            'order_id': order.id,
            'customer_id': order.customer_id,
            'customer_name': customer.name,  # Assuming you have the 'name' field in 'customer'
            'customer_address': order.address,  # Assuming 'address' exists in 'customer'
            'total_cost': order.total_cost,
            'status': order.status,
            'ordered_at': order.ordered_at.strftime('%Y-%m-%d %H:%M:%S'),
            'driver_ids': driver_ids,  # List of drivers assigned to this order
            'items': get_item_from_order(order),
        }
        order_list.append(order_info)

    return jsonify(order_list)

def get_item_from_order(order):
    item_list = []
    for sub_order in order.sub_orders:
        ingredients = OrderedIngredient.query.filter_by(sub_order_id=sub_order.id).all()
        ingredient_details = [{'name': ingredient.ingredient.name, 'action': ingredient.action} for ingredient in ingredients]

        item_info = {
            'item_id': sub_order.item_id,
            'name': sub_order.menu_item.name,
            'ingredients': ingredient_details,
            'quantity': sub_order.quantity,
        }
        item_list.append(item_info)
    return item_list

# Add a new menu item
@admin_bp.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    category = data.get('category')

    if not name or not price or not category:
        return jsonify({'error': 'Missing required fields'}), 400

    new_item = Menu(name=name, price=price, category=category)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Menu item added', 'item_id': new_item.id}), 201

# Update a menu item
@admin_bp.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.get_json()
    item = Menu.query.get_or_404(item_id)

    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.category = data.get('category', item.category)

    db.session.commit()
    return jsonify({'message': 'Menu item updated'})

# Delete a menu item
@admin_bp.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    # Check if the menu item is part of any active orders
    active_sub_orders = SubOrder.query.filter_by(item_id=item_id).first()
    active_cart_items = CartItem.query.filter_by(menu_id=item_id).first()
    
    if active_sub_orders:
        return jsonify({
            'error': f'Menu item {item_id} cannot be deleted because it is part of an active orders.'
        }), 400

    if active_cart_items:
        return jsonify({
            'error': f'Menu item {item_id} cannot be deleted because it is part of an active cart items.'
        }), 400

    # If no references found, proceed with deletion
    item = Menu.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Menu item deleted successfully'})

# Update order status
@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()

    # Validate that 'status' is in the request data
    status = data.get('status')
    if not status:
        return jsonify({'error': 'Status is required'}), 400

    # Check if status is one of the valid options that match your UI
    valid_statuses = ['Pending', 'In Preparation', 'In Delivery', 'Delivered', 'Cancelled']
    if status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400

    # Get the order by ID, or return a 404 if not found
    order = CustomerOrders.query.get_or_404(order_id)

    # Update the order status
    try:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated', 'order_id': order_id, 'new_status': status}), 200
    except Exception as e:
        db.session.rollback()  # In case of error, roll back any changes
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Update order delivery ETA
@admin_bp.route('/orders/<int:order_id>/eta', methods=['PUT'])
def update_order_eta(order_id):
    data = request.get_json()
    order = CustomerOrders.query.get_or_404(order_id)

    delivery_eta = data.get('delivery_eta')

    if not delivery_eta:
        return jsonify({'error': 'Missing delivery ETA'}), 400

    order.delivery_eta = delivery_eta
    db.session.commit()
    return jsonify({'message': 'Order delivery ETA updated'})

# Get all delivery drivers
@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    drivers = DeliveryDriver.query.all()
    driver_list = []
    for driver in drivers:
        driver_info = {
            'driver_id': driver.id,
            'delivery_area': driver.delivery_area,
            'last_delivery': driver.last_delivery.strftime('%Y-%m-%d %H:%M:%S') if driver.last_delivery else None,
        }
        driver_list.append(driver_info)
    return jsonify(driver_list)

# Add a new delivery driver
@admin_bp.route('/drivers', methods=['POST'])
def add_driver():
    data = request.get_json()
    delivery_area = data.get('delivery_area')

    if not delivery_area:
        return jsonify({'error': 'Missing required fields'}), 400

    new_driver = DeliveryDriver(delivery_area=delivery_area)
    db.session.add(new_driver)
    db.session.commit()

    return jsonify({'message': 'Delivery driver added', 'driver_id': new_driver.id}), 201

# Update a delivery driver
@admin_bp.route('/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    data = request.get_json()
    driver = DeliveryDriver.query.get_or_404(driver_id)

    driver.delivery_area = data.get('delivery_area', driver.delivery_area)

    db.session.commit()
    return jsonify({'message': 'Delivery driver updated'})

# Delete a delivery driver
@admin_bp.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = DeliveryDriver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({'message': 'Delivery driver deleted'})
