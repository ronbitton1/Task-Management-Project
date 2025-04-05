from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if mongo.db.users.find_one({"username": username}):
        return {"error": "User already exists"}, 400

    hashed = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed})
    return {"message": "User registered"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return {"error": "Invalid credentials"}, 401

    return {"message": "Login successful", "username": username}, 200
