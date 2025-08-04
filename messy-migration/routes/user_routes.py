from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.security import hash_password, check_password, is_valid_email, is_strong_password

conn = get_db_connection()
cursor = conn.cursor()

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def home():
    return "User Management System", 200

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users), 200

@user_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not (name and email and password):
            return jsonify({"error": "Missing name, email, or password"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        if not is_strong_password(password):
            return jsonify({"error": "Password too short"}), 400

        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, hashed_password))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not (name and email):
            return jsonify({"error": "Missing name or email"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                       (name, email, user_id))
        conn.commit()
        return jsonify({"message": "User updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({"message": f"User {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f'%{name}%',))
    users = cursor.fetchall()
    return jsonify(users), 200

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            return jsonify({"error": "Missing email or password"}), 400

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password(password, user[3]):
            return jsonify({"status": "success", "user_id": user[0]}), 200
        else:
            return jsonify({"status": "failed"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
