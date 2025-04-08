import os
from flask import Flask, session, render_template, send_from_directory
from flask_cors import CORS
from db import init_db
from auth_routes import auth_bp
from task_routes import task_bp
from ai_routes import ai_bp
from datetime import timedelta
from limiter_config import limiter
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("voltify.log"),
        logging.StreamHandler()
    ]
)

# Serve frontend
app = Flask(__name__, static_folder="static", template_folder="templates")

# For production: replace localhost with deployed domain
CORS(app, origins=["*"], supports_credentials=True)

init_db(app)
limiter.init_app(app)

app.secret_key = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

if os.environ.get("FLASK_ENV") == "production":
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "None"
else:
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = None  # Let the browser infer domain

# Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")
app.register_blueprint(ai_bp, url_prefix="/api/ai")

# Serve frontend index.html
@app.route("/")
def index():
    return render_template("index.html")

# Serve static files (JS/CSS)
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@app.after_request
def log_cors_headers(response):
    print("➡️ Access-Control-Allow-Credentials:", response.headers.get("Access-Control-Allow-Credentials"))
    print("➡️ Access-Control-Allow-Origin:", response.headers.get("Access-Control-Allow-Origin"))
    print("➡️ Response status code:", response.status_code)
    return response

if __name__ == "__main__":
    # Run publicly on port 5000
    app.run(debug=False, host="0.0.0.0", port=5000)
