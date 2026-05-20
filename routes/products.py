from flask import Blueprint, jsonify, request
from database import get_db

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def get_products():
    db = get_db()
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    if search:
        rows = db.execute('SELECT * FROM products WHERE name LIKE ? OR description LIKE ?', (f'%{search}%', f'%{search}%')).fetchall()
    elif category:
        rows = db.execute('SELECT * FROM products WHERE category=?', (category,)).fetchall()
    else:
        rows = db.execute('SELECT * FROM products').fetchall()
    return jsonify({'success': True, 'products': [{'id': r['id'], 'name': r['name'], 'description': r['description'], 'price': r['price'], 'original_price': r['original_price'], 'stock': r['stock'], 'category': r['category'], 'image_url': r['image_url'], 'image2': r['image2'], 'image3': r['image3'], 'image4': r['image4'], 'rating': r['rating'], 'reviews': r['reviews'], 'badge': r['badge']} for r in rows]})

@products_bp.route('/products/<int:pid>')
def get_product(pid):
    db = get_db()
    r = db.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
    if not r:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    return jsonify({'success': True, 'product': {'id': r['id'], 'name': r['name'], 'description': r['description'], 'price': r['price'], 'original_price': r['original_price'], 'stock': r['stock'], 'category': r['category'], 'image_url': r['image_url'], 'image2': r['image2'], 'image3': r['image3'], 'image4': r['image4'], 'rating': r['rating'], 'reviews': r['reviews'], 'badge': r['badge']}})

@products_bp.route('/categories')
def get_categories():
    db = get_db()
    rows = db.execute('SELECT DISTINCT category FROM products').fetchall()
    return jsonify({'success': True, 'categories': [r['category'] for r in rows]})
