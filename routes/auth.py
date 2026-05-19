from flask import Blueprint, jsonify, request
from database import get_db
import hashlib
auth_bp = Blueprint('auth', __name__)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'All fields required'}), 400
    db = get_db()
    existing = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
    if existing:
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
    db.execute('INSERT INTO users (name, email, password) VALUES (?,?,?)', (name, email, hash_password(password)))
    db.commit()
    return jsonify({'success': True, 'message': 'Account created successfully'}), 201
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email=? AND password=?', (email, hash_password(password))).fetchone()
    if not user:
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    return jsonify({'success': True, 'message': 'Login successful', 'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}})
