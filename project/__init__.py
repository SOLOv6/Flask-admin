# Libraries
from flask import Flask, g, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# SQLite Settings
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


db = SQLAlchemy()
migrate = Migrate()


# Error Handlers
def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500


def create_app():
    print('run: create_app()')
    app = Flask(__name__)


    ''' Flask Configs '''
    app.config.from_envvar('APP_CONFIG_FILE')


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

    
    ''' Error Handler '''
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)


    return app