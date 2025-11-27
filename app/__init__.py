# For the App to make it a package.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
     
    # Import blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
    
    return app