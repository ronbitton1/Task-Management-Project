from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo
from logic.validators import validate_user_input

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    valid, error = validate_user_input(data, ["username", "password"])
    if not valid:
        return {"error": error}, 400

    username = data["username"]
    password = data["password"]

    if mongo.db.users.find_one({"username": username}):
        return {"error": "User already exists"}, 400

    hashed = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed})
    return {"message": "User registered"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    valid, error = validate_user_input(data, ["username", "password"])
    if not valid:
        return {"error": error}, 400

    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return {"error": "Invalid credentials"}, 401

    session["username"] = data["username"]
    session.permanent = True  # Make it expire after timeout
    return {"message": "Login successful", "username": data["username"]}, 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return {"message": "Logged out"}, 200
 