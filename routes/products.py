from flask import Blueprint, jsonify, request, send_from_directory
from database import get_db
import os
products_bp = Blueprint('products', __name__)
os.makedirs('product_images', exist_ok=True)
@products_bp.route('/products')
def get_products():
    db = get_db()
    rows = db.execute('SELECT * FROM products').fetchall()
    return jsonify({'success':True,'products':[{'id':r['id'],'name':r['name'],'description':r['description'],'price':r['price'],'stock':r['stock'],'category':r['category'],'image_url':r['image_url']} for r in rows]})
@products_bp.route('/products/<int:pid>')
def get_product(pid):
    db = get_db()
    r = db.execute('SELECT * FROM products WHERE id=?',(pid,)).fetchone()
    if not r: return jsonify({'success':False,'error':'Not found'}),404
    return jsonify({'success':True,'product':{'id':r['id'],'name':r['name'],'description':r['description'],'price':r['price'],'stock':r['stock'],'category':r['category'],'image_url':r['image_url']}})
@products_bp.route('/categories')
def get_categories():
    db = get_db()
    rows = db.execute('SELECT DISTINCT category FROM products').fetchall()
    return jsonify({'success':True,'categories':[r['category'] for r in rows]})
@products_bp.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('product_images', filename)
