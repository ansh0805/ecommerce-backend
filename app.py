from flask import Flask, g
from flask_cors import CORS
from database import init_db, close_db
from routes.products import products_bp
from routes.cart import cart_bp
from routes.auth import auth_bp
app = Flask(__name__)
app.secret_key = 'ecommerce-secret-key'
CORS(app)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(auth_bp)
app.teardown_appcontext(close_db)
with app.app_context():
    init_db()
@app.route('/')
def home():
    return {'message': 'Ecommerce API is running!'}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
