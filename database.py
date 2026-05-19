import sqlite3
from flask import g
DATABASE = 'ecommerce.db'
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, stock INTEGER DEFAULT 0, category TEXT, image_url TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, cart_id TEXT NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER DEFAULT 1)')
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
    cur.execute('SELECT COUNT(*) FROM products')
    if cur.fetchone()[0] == 0:
        cur.executemany('INSERT INTO products (name,description,price,stock,category,image_url) VALUES (?,?,?,?,?,?)', [('Wireless Headphones','Premium noise-cancelling headphones',2999.0,50,'Electronics','https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'),('Running Shoes','Lightweight running shoes',1499.0,30,'Footwear','https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'),('Cotton T-Shirt','100% premium cotton t-shirt',499.0,100,'Clothing','https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'),('Water Bottle','Insulated water bottle',799.0,75,'Accessories','https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400'),('Laptop Backpack','Waterproof backpack',1999.0,40,'Bags','https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'),('Smart Watch','Fitness tracker with GPS',3499.0,20,'Electronics','https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'),('Sunglasses','UV400 polarised sunglasses',899.0,60,'Accessories','https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400'),('Yoga Mat','Non-slip exercise mat',699.0,45,'Sports','https://images.unsplash.com/photo-1601925228869-d3ee2622f9de?w=400'),('Mechanical Keyboard','RGB gaming keyboard',4999.0,25,'Electronics','https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400'),('Denim Jacket','Classic blue denim jacket',2499.0,35,'Clothing','https://images.unsplash.com/photo-1543087903-1ac2ec7aa8c5?w=400'),('Coffee Maker','12 cup programmable coffee maker',3999.0,15,'Kitchen','https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400'),('Sneakers','Classic white leather sneakers',1999.0,50,'Footwear','https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400')])
    conn.commit()
    conn.close()
    print('Database initialised.')
