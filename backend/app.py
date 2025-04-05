from flask import Flask
from flask_cors import CORS
from db import init_db
from auth_routes import auth_bp
from task_routes import task_bp
from ai_routes import ai_bp

app = Flask(__name__)
CORS(app)
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")
app.register_blueprint(ai_bp, url_prefix="/api/ai")

@app.route("/")
def index():
    return {"message": "Voltify Task Manager API"}, 200

if __name__ == "__main__":
    app.run(debug=True)
