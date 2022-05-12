# Libraries
from flask import Flask, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Flask configs
import config


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
    from .models import car
    from .models import user
    from .models import event


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