# libraries
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# flask configs
import config

# DB
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    print('run: create_app()')
    app = Flask(__name__)


    ''' Flask Configs '''
    app.config.from_object(config)


    ''' DB INIT '''
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    from project.models import models


    ''' Routes INIT '''
    from project.routes import base_routes
    from project.routes import auth_routes
    app.register_blueprint(base_routes.blueprint)
    app.register_blueprint(auth_routes.blueprint)


    ''' Rest-x INIT '''
    from project.apis import blueprint as api
    app.register_blueprint(api)


    return app