from flask import Flask
from .utils import db
from flask_migrate import Migrate
from flask_restx import Api, Namespace
from Api.models.notes import Note
from Api.models.user import User  
from .auth.user import auth_namespace
from .resources.note import note_namespace
from .config.config import config_dict
from flask_jwt_extended import JWTManager

def create_app(config=config_dict["dev"]):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt=JWTManager(app)
    
    migrate=Migrate(app, db)
    
    api = Api(app)
    api.add_namespace(note_namespace, path="/notes")
    api.add_namespace(auth_namespace, path='/auth')


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "user":User,
            "note":Note
        }

    return app