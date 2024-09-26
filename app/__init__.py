from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    print(f"app.root_path: {app.root_path}")
    print(f"app.template_folder: {app.template_folder}")
    print(f"app.jinja_loader.searchpath: {app.jinja_loader.searchpath}")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.configure_mappers()

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.blueprints.auth import auth_bp
    from app.blueprints.devices import devices_bp
    from app.blueprints.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(main_bp)

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def forbidden_error(error):
        return render_template('404.html'), 403

    return app