from flask import Blueprint, jsonify, request, g
from database import get_db
import json
import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    cart_id = request.headers.get('X-Cart-ID', '')
    db = get_db()
    rows = db.execute('SELECT * FROM orders WHERE cart_id=? ORDER BY id DESC', (cart_id,)).fetchall()
    return jsonify({'success': True, 'orders': [dict(r) for r in rows]})

@orders_bp.route('/orders', methods=['POST'])
def place_order():
    cart_id = request.headers.get('X-Cart-ID', '')
    db = get_db()
    data = request.get_json()
    address = data.get('address', '')
    payment = data.get('payment', 'COD')
    cart_items = db.execute(
        'SELECT c.quantity, p.name, p.price, p.image_url FROM cart c JOIN products p ON c.product_id=p.id WHERE c.cart_id=?',
        (cart_id,)
    ).fetchall()
    if not cart_items:
        return jsonify({'success': False, 'error': 'Cart is empty'}), 400
    total = sum(float(r['price']) * int(r['quantity']) for r in cart_items)
    items_json = json.dumps([{
        'name': r['name'],
        'price': float(r['price']),
        'quantity': int(r['quantity']),
        'image_url': r['image_url']
    } for r in cart_items])
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    db.execute(
        'INSERT INTO orders (cart_id, items, total, address, payment, status, created_at) VALUES (?,?,?,?,?,?,?)',
        (cart_id, items_json, total, address, payment, 'Confirmed', now)
    )
    db.execute('DELETE FROM cart WHERE cart_id=?', (cart_id,))
    db.commit()
    return jsonify({'success': True, 'message': 'Order placed successfully!', 'total': total})
