### task_routes.py
from flask import Blueprint, request, session
from db import mongo
from bson import ObjectId
from datetime import datetime
from logic.validators import validate_user_input
from logic.task_utills import is_task_overdue
from logic.telegram_notifier import send_telegram_message
from logic.ai_helpers import parse_openai_response
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

task_bp = Blueprint("tasks", __name__)

def serialize_task(task):
    task["_id"] = str(task["_id"])
    return task

@task_bp.route("/", methods=["GET"])
def get_tasks():
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    query = {"user": username}
    if "status" in request.args:
        query["status"] = request.args["status"]
    if "category" in request.args:
        query["category"] = request.args["category"]

    tasks = mongo.db.tasks.find(query)
    return [serialize_task(t) for t in tasks], 200

@task_bp.route("/", methods=["POST"])
def create_task():
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    valid, error = validate_user_input(data, ["title", "description", "due_date"])
    if not valid:
        return {"error": error}, 400

    task = {
        "user": username,
        "title": data["title"],
        "description": data["description"],
        "due_date": data["due_date"],
        "created_at": datetime.utcnow().isoformat(),
        "status": "open",
        "category": data.get("category", ""),
        "estimated_time": data.get("estimated_time", "")
    }

    result = mongo.db.tasks.insert_one(task)
    task["_id"] = str(result.inserted_id)

    user = mongo.db.users.find_one({"username": username})
    if user and user.get("telegram_chat_id"):
        message = f"📝 New task created: '{task['title']}' due on {task['due_date']}"
        send_telegram_message(message, user["telegram_chat_id"])

    return task, 201

@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user": username})
    if not task:
        return {"error": "Task not found"}, 404

    return serialize_task(task), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id), "user": username})
    if not task:
        return {"error": "Task not found"}, 404

    updates = {k: v for k, v in data.items() if k in ["title", "description", "due_date", "status", "category", "estimated_time"]}
    mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": updates})

    if task["status"] != "done" and updates.get("status") == "done":
        user = mongo.db.users.find_one({"username": username})
        if user and user.get("telegram_chat_id"):
            message = f"✅ Task marked as done: '{task['title']}'"
            send_telegram_message(message, user["telegram_chat_id"])

    updated_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    return serialize_task(updated_task), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user": username})
    if result.deleted_count == 0:
        return {"error": "Task not found or not authorized"}, 404

    return {"message": "Task deleted"}, 200

@task_bp.route("/weekly-summary", methods=["POST"])
def send_weekly_summary():
    users = mongo.db.users.find({"telegram_chat_id": {"$exists": True}})
    for user in users:
        username = user["username"]
        chat_id = user["telegram_chat_id"]
        tasks = list(mongo.db.tasks.find({"user": username, "status": "open"}))
        if not tasks:
            continue
        task_descriptions = "\n".join([f"- {t['title']} (due {t['due_date']})" for t in tasks])
        prompt = f"Summarize and categorize these tasks with time estimates:\n{task_descriptions}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            summary = parse_openai_response(response)
            send_telegram_message(f"📊 Weekly Summary:\n{summary}", chat_id)
        except Exception as e:
            print(f"Failed to send summary to {username}: {e}")
    return {"message": "Summaries sent"}, 200

@task_bp.route("/update-chat-id", methods=["POST"])
def update_telegram_chat_id():
    username = session.get("username")
    if not username:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    chat_id = data.get("telegram_chat_id")
    if not chat_id:
        return {"error": "Missing telegram_chat_id"}, 400

    mongo.db.users.update_one({"username": username}, {"$set": {"telegram_chat_id": chat_id}})
    return {"message": "Telegram chat ID updated"}, 200
