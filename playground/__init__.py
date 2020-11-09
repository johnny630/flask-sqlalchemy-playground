# python core
import os

# flask relative
from flask import Flask, g
from flask.cli import with_appcontext

# extensions
import click
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade, migrate




dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    print(dotenv_path)
    load_dotenv(dotenv_path, override=True)

db = SQLAlchemy()
migrates = Migrate()

def create_app():
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV', default = 'development')

    from .config import config
    app.config.from_object(config[config_name])

    print(f'config_name: {config_name}')
    print(app.config)

    db.init_app(app)
    migrates.init_app(app, db)

    from .models.comment import Comment
    from .models.user import User
    from .models.post import Post, Category

    @app.shell_context_processor
    def make_shell_context():
        from . import models
        return dict(Post=Post, Category=Category, models=models, db=db)

    return app
