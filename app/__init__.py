from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')
    
    db.init_app(app)

    login_manager.init_app(app)

    return app

