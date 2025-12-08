from flask import Flask
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()

def create_app(config_name='development'):
    """Application factory."""
    app = Flask(__name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    
    # Load configuration
    from backend.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from backend.app.routes import auth_bp, dashboard_bp, activity_bp, nutrition_bp, goals_bp, gamification_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(gamification_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Root route: redirect to dashboard if logged in, otherwise show landing page
    @app.route('/')
    def home_redirect():
        from flask import render_template
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('landing.html')

    # Serve favicon.ico requests by redirecting to the SVG in static
    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.svg'))
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}
    
    return app
