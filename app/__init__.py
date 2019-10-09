from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
login.login_view = 'login'


def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.api import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app import models, errors

    return app

