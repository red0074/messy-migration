from flask import Blueprint, request, jsonify
from app.db import get_db
from app.utils import hash_password

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def home():
    return "User Management System"

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    db = get_db()
    users = db.execute("SELECT id, name, email FROM users").fetchall()
    return jsonify([dict(user) for user in users])

@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    user = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_pw = hash_password(password)
    db = get_db()
    db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
    db.commit()

    return jsonify({"message": "User created successfully"}), 201

@user_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not all([name, email]):
        return jsonify({"error": "Missing fields"}), 400

    db = get_db()
    db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    db.commit()

    return jsonify({"message": "User updated"})

@user_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted"})

@user_bp.route("/search", methods=["GET"])
def search_users():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Name parameter required"}), 400

    db = get_db()
    users = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    return jsonify([dict(user) for user in users])

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()

    if user:
        return jsonify({"status": "success", "user_id": user["id"]})
    return jsonify({"status": "failed"}), 401
