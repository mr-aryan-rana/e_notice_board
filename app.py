# e_notice_board/app.py
from flask import Flask, redirect, url_for
from config import Config
from models.base import db
from datetime import datetime

# Blueprints
from routes.admin_routes import admin_bp
from routes.monitor_routes import monitor_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(monitor_bp, url_prefix='/monitor')
    
    # Template filter for current UTC time
    @app.template_filter('utcnow')
    def utcnow_filter(_):
        return datetime.utcnow()
    
    @app.route('/')
    def index():
        return redirect(url_for('admin.login'))

    # Database setup
    with app.app_context():
        db.create_all()
        _create_default_admin(app)

    # Start background checker for expired notices
    from utils.scheduler import start_background_checker
    start_background_checker(app)  # Pass app instance

    return app


def _create_default_admin(app):
    """Create a default admin user if none exists."""
    from models.admin_model import Admin
    
    if not Admin.query.first():
        default_admin = Admin(
            username='admin',
            email='admin@example.com'   # 👈 Add this
        )
        default_admin.set_password('admin123')
        db.session.add(default_admin)
        db.session.commit()
        app.logger.info("✅ Default admin created: username='admin', password='admin123'")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
