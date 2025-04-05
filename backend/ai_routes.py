from flask import Blueprint, request
import openai
import os

ai_bp = Blueprint("ai", __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    description = data.get("description", "")

    if not description:
        return {"error": "Missing task description"}, 400

    prompt = f"Categorize and estimate time for the following task: '{description}'"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        result = response["choices"][0]["message"]["content"]
        return {"recommendation": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500
