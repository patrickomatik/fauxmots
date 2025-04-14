import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'fauxmots.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        EMAIL_STORAGE_PATH=os.path.join(os.path.dirname(app.root_path), 'emails'),
        SMTP_HOST='127.0.0.1',
        SMTP_PORT=1025,
    )

    # Load instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure email storage directory exists
    try:
        os.makedirs(app.config['EMAIL_STORAGE_PATH'])
    except OSError:
        pass

    # Initialize database
    db.init_app(app)

    # Import models to ensure they're loaded before creating tables
    from .models import Email

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
