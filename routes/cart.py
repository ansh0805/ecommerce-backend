from flask import Blueprint, jsonify, request
from database import get_db
cart_bp = Blueprint('cart', __name__)
def get_cart_id():
    c = request.headers.get('X-Cart-ID')
    if not c: return None,jsonify({'success':False,'error':'X-Cart-ID required'}),400
    return c,None,None
@cart_bp.route('/cart')
def get_cart():
    cart_id,err,code = get_cart_id()
    if err: return err,code
    db = get_db()
    rows = db.execute('SELECT c.id as cid,c.quantity,p.id as pid,p.name,p.price,p.image_url FROM cart c JOIN products p ON c.product_id=p.id WHERE c.cart_id=?',(cart_id,)).fetchall()
    items=[{'cart_item_id':r['cid'],'product_id':r['pid'],'name':r['name'],'price':r['price'],'quantity':r['quantity'],'subtotal':round(r['price']*r['quantity'],2),'image_url':r['image_url']} for r in rows]
    return jsonify({'success':True,'items':items,'total':round(sum(i['subtotal'] for i in items),2)})
@cart_bp.route('/cart/add',methods=['POST'])
def add_to_cart():
    cart_id,err,code = get_cart_id()
    if err: return err,code
    data = request.get_json()
    pid = data.get('product_id')
    qty = int(data.get('quantity',1))
    db = get_db()
    p = db.execute('SELECT * FROM products WHERE id=?',(pid,)).fetchone()
    if not p: return jsonify({'success':False,'error':'Not found'}),404
    ex = db.execute('SELECT * FROM cart WHERE cart_id=? AND product_id=?',(cart_id,pid)).fetchone()
    if ex:
        db.execute('UPDATE cart SET quantity=? WHERE id=?',(ex['quantity']+qty,ex['id']))
    else:
        db.execute('INSERT INTO cart (cart_id,product_id,quantity) VALUES (?,?,?)',(cart_id,pid,qty))
    db.commit()
    return jsonify({'success':True,'message':str(p['name'])+' added to cart'})
@cart_bp.route('/cart/remove/<int:iid>',methods=['DELETE'])
def remove_from_cart(iid):
    cart_id,err,code = get_cart_id()
    if err: return err,code
    db = get_db()
    db.execute('DELETE FROM cart WHERE id=? AND cart_id=?',(iid,cart_id))
    db.commit()
    return jsonify({'success':True,'message':'Removed'})
@cart_bp.route('/cart/clear',methods=['DELETE'])
def clear_cart():
    cart_id,err,code = get_cart_id()
    if err: return err,code
    db = get_db()
    db.execute('DELETE FROM cart WHERE cart_id=?',(cart_id,))
    db.commit()
    return jsonify({'success':True,'message':'Cart cleared'})
