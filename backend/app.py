import os
from flask import Flask
from flask_cors import CORS
from db import init_db
from auth_routes import auth_bp
from task_routes import task_bp
from ai_routes import ai_bp
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("voltify.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)
init_db(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per hour"])


app.secret_key = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(task_bp, url_prefix="/api/tasks")
app.register_blueprint(ai_bp, url_prefix="/api/ai")

@app.route("/")
def index():
    return {"message": "Voltify Task Manager API"}, 200

if __name__ == "__main__":
    app.run(debug=True)
