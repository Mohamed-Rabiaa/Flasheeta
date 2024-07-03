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
    """ create_app """
    from config import Config

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app_config = Config()
    app.config.from_object(app_config)
    # Log the SECRET_KEY to ensure it's being set correctly
    app.logger.debug(f"SECRET_KEY: {app.config['SECRET_KEY']}")
    csrf.init_app(app)
    db.init_app(app)
    app.storage = DBStorage(db)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    with app.app_context():
        # app.storage.reload()
        db.create_all()
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

    return app

from flask import current_app as app

@login_manager.user_loader
def load_user(user_id):
    """ load_user """
    from app.models.user import User
    return app.storage.get(User, user_id)

'''
with app.app_context():
    @app.teardown_appcontext
    def close_db():
        """ close_db """
        app.storage.close()
'''
