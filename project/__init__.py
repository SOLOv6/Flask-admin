# Libraries
from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Flask configs
import config

# SQLite Settings
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    print('run: create_app()')
    app = Flask(__name__)


    ''' Flask Configs '''
    app.config.from_object(config)


    ''' DB INIT '''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from .models import car
    from .models import user
    from .models import event
    from .models import entry


    ''' Routes INIT '''
    from project.routes import base_routes, auth_routes, car_routes, user_routes
    app.register_blueprint(base_routes.blueprint)
    app.register_blueprint(auth_routes.blueprint)
    app.register_blueprint(car_routes.blueprint)
    app.register_blueprint(user_routes.blueprint)


    ''' Rest-x INIT '''
    from project.apis import blueprint as api
    app.register_blueprint(api)


    ''' Request Hook '''
    @app.before_request
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()


    return app