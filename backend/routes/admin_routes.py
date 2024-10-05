from flask import Blueprint, jsonify, request
from models.database import Menu, CustomerOrders, DeliveryDriver
from app import db

admin_bp = Blueprint('admin_bp', __name__)

# Get all menu items
@admin_bp.route('/menu', methods=['GET'])
def get_menu():
    items = Menu.query.all()
    menu = [{'id': item.id, 'name': item.name, 'price': item.price, 'category': item.category} for item in items]
    return jsonify(menu)

@admin_bp.route('/orders', methods=['GET'])
def get_all_orders():
    orders = CustomerOrders.query.all()
    order_list = []
    for order in orders:
        order_info = {
            'order_id': order.id,
            'customer_id': order.customer_id,
            'total_cost': order.total_cost,
            'status': order.status,
            'ordered_at': order.ordered_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        order_list.append(order_info)
    return jsonify(order_list)

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
    item = Menu.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Menu item deleted'})

# Update order status
@admin_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    order = CustomerOrders.query.get_or_404(order_id)

    status = data.get('status')

    if status not in ['Pending', 'Preparing', 'Out for delivery', 'Delivered']:
        return jsonify({'error': 'Invalid status'}), 400

    order.status = status
    db.session.commit()
    return jsonify({'message': 'Order status updated'})

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

# Delete an order (for some reason)
@admin_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = CustomerOrders.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted from system (for some reason)'})

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

    new_driver = DeliveryDriver(delivery_area=delivery_area, last_delivery=None)
    db.session.add(new_driver)
    db.session.commit()

    return jsonify({'message': 'Delivery driver added', 'driver_id': new_driver.id}), 201

# Delete a delivery driver
@admin_bp.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = DeliveryDriver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({'message': 'Delivery driver deleted'})
