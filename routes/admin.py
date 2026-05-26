from flask import Blueprint, jsonify, request
from database import get_db
admin_bp = Blueprint('admin', __name__)
ADMIN_KEY = 'shopeasy-admin-2024'
def check_admin(req):
    return req.headers.get('X-Admin-Key') == ADMIN_KEY
@admin_bp.route('/admin/products', methods=['GET'])
def admin_get_products():
    if not check_admin(request): return jsonify({'success':False,'error':'Unauthorized'}),401
    db = get_db()
    rows = db.execute('SELECT * FROM products').fetchall()
    return jsonify({'success':True,'products':[{'id':r['id'],'name':r['name'],'price':r['price'],'stock':r['stock'],'category':r['category'],'image_url':r['image_url']} for r in rows]})
@admin_bp.route('/admin/products/add', methods=['POST'])
def admin_add_product():
    if not check_admin(request): return jsonify({'success':False,'error':'Unauthorized'}),401
    data = request.get_json()
    name = data.get('name')
    description = data.get('description','')
    price = float(data.get('price',0))
    original_price = float(data.get('original_price', price))
    stock = int(data.get('stock',0))
    category = data.get('category','General')
    image_url = data.get('image_url','')
    badge = data.get('badge','')
    if not name or price <= 0:
        return jsonify({'success':False,'error':'Name and price required'}),400
    db = get_db()
    cur = db.execute('INSERT INTO products (name,description,price,original_price,stock,category,image_url,badge) VALUES (?,?,?,?,?,?,?,?)',(name,description,price,original_price,stock,category,image_url,badge))
    db.commit()
    return jsonify({'success':True,'message':'Product added','id':cur.lastrowid}),201
@admin_bp.route('/admin/products/update/<int:pid>', methods=['PUT'])
def admin_update_product(pid):
    if not check_admin(request): return jsonify({'success':False,'error':'Unauthorized'}),401
    data = request.get_json()
    db = get_db()
    db.execute('UPDATE products SET name=?,description=?,price=?,stock=?,category=?,image_url=?,badge=? WHERE id=?',(data.get('name'),data.get('description'),float(data.get('price',0)),int(data.get('stock',0)),data.get('category'),data.get('image_url'),data.get('badge',''),pid))
    db.commit()
    return jsonify({'success':True,'message':'Product updated'})
@admin_bp.route('/admin/products/delete/<int:pid>', methods=['DELETE'])
def admin_delete_product(pid):
    if not check_admin(request): return jsonify({'success':False,'error':'Unauthorized'}),401
    db = get_db()
    db.execute('DELETE FROM products WHERE id=?',(pid,))
    db.commit()
    return jsonify({'success':True,'message':'Product deleted'})
@admin_bp.route('/admin/stats', methods=['GET'])
def admin_stats():
    if not check_admin(request): return jsonify({'success':False,'error':'Unauthorized'}),401
    db = get_db()
    total_products = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    total_users = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_orders = db.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    total_revenue = db.execute('SELECT SUM(total) FROM orders').fetchone()[0] or 0
    return jsonify({'success':True,'stats':{'total_products':total_products,'total_users':total_users,'total_orders':total_orders,'total_revenue':total_revenue}})
