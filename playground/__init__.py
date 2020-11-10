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
from faker import Faker



dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    print(dotenv_path)
    load_dotenv(dotenv_path, override=True)

db = SQLAlchemy()
migrates = Migrate()
fake = Faker()

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

    @app.route('/clear_all_data')
    def clear_all_data():
        # https://myapollo.com.tw/zh-tw/sqlalchemy-truncate-tables/
        # https://gist.github.com/vkotovv/6281951
        # https://stackoverflow.com/questions/38112379/disable-postgresql-foreign-key-checks-for-migrations  postgresql foreign-key-checks
        db.session.execute("SET session_replication_role = 'replica';")
        # print(db.metadata.sorted_tables)
        for table in db.metadata.sorted_tables:
            print('Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.execute("SET session_replication_role = 'origin';")
        db.session.commit()

        return 'ok'

    @app.route('/seed')
    def generate_data():
        # Create
        computer_category = Category(name='computer')
        life_category = Category(name='life')
        post1 = Post(title='title1', body='', category=computer_category)
        post2 = Post(title='title2', body='', category=computer_category)
        post3 = Post(title='title1', body='', category=life_category)

        db.session.add_all([post1, post2, post3])
        db.session.commit()

        return 'ok'

    return app
