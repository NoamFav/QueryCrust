# routes/admin_routes.py
from flask import Blueprint, jsonify, request
from models.database import Menu, CustomerOrders, DeliveryDriver, OrderedIngredient, SubOrder, CartItem, Delivery
from models import db

admin_bp = Blueprint('admin_bp', __name__)

# Get all menu items
@admin_bp.route('/menu', methods=['GET'])
def get_menu():
    items = Menu.query.all()
    # Convert the list of items to a list of dictionaries for JSON serialization
    menu = [{'id': item.id, 'name': item.name, 'price': item.price, 'category': item.category} for item in items]
    return jsonify(menu)

# Get all orders
@admin_bp.route('/orders', methods=['GET'])
def get_all_orders():
    orders = CustomerOrders.query.all()
    order_list = []

    # Go through each order and get the details 
    for order in orders:
        customer = order.customer
        
        # Get the list of drivers who delivered the order
        deliveries = Delivery.query.filter_by(order_id=order.id).all()
        driver_ids = [delivery.delivered_by for delivery in deliveries]

        # Put everything together in a dictionary
        order_info = {
            'order_id': order.id,
            'customer_id': order.customer_id,
            'customer_name': customer.name,
            'customer_address': order.address,
            'total_cost': order.total_cost,
            'status': order.status,
            'ordered_at': order.ordered_at.strftime('%Y-%m-%d %H:%M:%S'), # Convert datetime to string in format 'YYYY-MM-DD HH:MM:SS'
            'driver_ids': driver_ids,
            'items': get_item_from_order(order),
        }
        order_list.append(order_info)

    return jsonify(order_list)

# Helper function to get the items in an order
def get_item_from_order(order):

    # Initialize an empty list to store the items
    item_list = []

    # Go through each sub-order in the order and get the details
    for sub_order in order.sub_orders:
        # Get the ingredients for the sub-order
        ingredients = OrderedIngredient.query.filter_by(sub_order_id=sub_order.id).all()
        ingredient_details = [{'name': ingredient.ingredient.name, 'action': ingredient.action} for ingredient in ingredients]

        # Put everything together in a dictionary for the item
        item_info = {
            'item_id': sub_order.item_id,
            'name': sub_order.menu_item.name,
            'ingredients': ingredient_details,
            'quantity': sub_order.quantity,
        }
        item_list.append(item_info)
    return item_list

# Removed methods to add, and update menu item_list
# Instead, you gotta use sql commands to do that
# It would be better to use a GUI to manage the database
# But I don't need them just yet

# Delete a menu item
@admin_bp.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):

    # Check if the menu item is part of an active order
    active_sub_orders = SubOrder.query.filter_by(item_id=item_id).first()
    active_cart_items = CartItem.query.filter_by(menu_id=item_id).first()
    
    # If the menu item is part of an active order, return an error
    if active_sub_orders:
        return jsonify({
            'error': f'Menu item {item_id} cannot be deleted because it is part of an active orders.'
        }), 400

    # If the menu item is part of an active cart item, return an error
    if active_cart_items:
        return jsonify({
            'error': f'Menu item {item_id} cannot be deleted because it is part of an active cart items.'
        }), 400

    # If the menu item is not part of an active order, delete it
    item = Menu.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Menu item deleted successfully'})

# Update order status
@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):

    # Get the new status from the request data
    data = request.get_json()

    # Check if the status is provided
    status = data.get('status')

    # If status is not provided, return an error
    if not status:
        return jsonify({'error': 'Status is required'}), 400

    # Check if the status is valid (one of the allowed statuses)
    valid_statuses = ['Pending', 'In Preparation', 'In Delivery', 'Delivered', 'Cancelled']
    
    # If status is not valid, return an error
    if status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400
    
    # Get the order from the database
    order = CustomerOrders.query.get_or_404(order_id)
    delivery = Delivery.query.filter_by(order_id=order_id).first()
    driver_ids = [delivery.delivered_by] if delivery else []

    try:
        # Update the status of the order
        order.status = status
        if status == 'Delivered':
            for driver_id in driver_ids:
                driver = DeliveryDriver.query.get_or_404(driver_id)
                if not driver:
                    return jsonify({'error': f'Delivery driver with ID {driver_id} not found'}), 404
                driver.last_delivery = order.ordered_at
        db.session.commit()
        return jsonify({'message': 'Order status updated', 'order_id': order_id, 'new_status': status}), 200
    except Exception as e:
        # If an error occurs, rollback the session and return an error message
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Get all delivery drivers
@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():

    # Get all delivery drivers from the database
    drivers = DeliveryDriver.query.all()

    # Initialize an empty list to store the driver details
    driver_list = []

    # Go through each driver and get the details
    for driver in drivers:
        driver_info = {
            'driver_id': driver.id,
            'delivery_area': driver.delivery_area,
            'last_delivery': driver.last_delivery.strftime('%Y-%m-%d %H:%M:%S') if driver.last_delivery else None,
        }
        driver_list.append(driver_info)

    # Return the list of drivers as JSON
    return jsonify(driver_list)

# Add a new delivery driver
@admin_bp.route('/drivers', methods=['POST'])
def add_driver():

    # Get the delivery area from the request data
    data = request.get_json()
    delivery_area = data.get('delivery_area') # Required field

    # If delivery area is not provided, return an error
    if not delivery_area:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new delivery driver with the provided delivery area
    new_driver = DeliveryDriver(delivery_area=delivery_area)
    db.session.add(new_driver) # Add the new driver to the session
    db.session.commit() # Commit the session to the database

    return jsonify({'message': 'Delivery driver added', 'driver_id': new_driver.id}), 201

# Update a delivery driver
@admin_bp.route('/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):

    # Get the delivery area from the request data
    data = request.get_json()

    # Get the delivery driver from the database
    driver = DeliveryDriver.query.get_or_404(driver_id)

    # Update the delivery area if provided
    driver.delivery_area = data.get('delivery_area', driver.delivery_area)

    db.session.commit()
    return jsonify({'message': 'Delivery driver updated'})

# Delete a delivery driver
@admin_bp.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):

    # Get the delivery driver from the database and delete it
    driver = DeliveryDriver.query.get_or_404(driver_id)
    db.session.delete(driver) # Delete the driver
    db.session.commit() # Commit the session to the database
    return jsonify({'message': 'Delivery driver deleted'})
