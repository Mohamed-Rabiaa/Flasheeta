from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager, logout_user
from flask_wtf import CSRFProtect
from app.models.engine.db_storage import DBStorage

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    """ Creates the application instance"""
    from config import Config

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app_config = Config()
    app.config.from_object(app_config)

    csrf.init_app(app)
    db.init_app(app)
    app.storage = DBStorage(db)
    login_manager.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    migrate.init_app(app, db)

    with app.app_context():
        # Creating the database tables
        db.create_all()

        # Register routes
        from app.web_routes import auth_routes, decks_routes, flashcards_routes, profile_routes
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(decks_routes.bp)
        app.register_blueprint(flashcards_routes.bp)
        app.register_blueprint(profile_routes.bp)

        #register the API blueprints
        from app.api.v1.views import index, users, decks, flashcards, progress
        app.register_blueprint(index.index_view)
        app.register_blueprint(users.users_view)
        app.register_blueprint(decks.decks_view)
        app.register_blueprint(flashcards.flashcards_view)
        app.register_blueprint(progress.progress_view)
        
        # Register error handlers
        from app.error_handlers import register_error_handlers
        register_error_handlers(app)

    return app

from flask import current_app as app

@login_manager.user_loader
def load_user(user_id):
    """ Loads the user """
    from app.models.user import User
    return app.storage.get(User, user_id)

'''
with app.app_context():
    @app.teardown_appcontext
    def close_db():
        """ close_db """
        app.storage.close()
'''
