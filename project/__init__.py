from flask import Flask


def create_app():
    print('run: create_app()')
    app = Flask(__name__)


    ''' Routes INIT '''
    from project.routes import base_routes
    from project.routes import auth_routes
    app.register_blueprint(base_routes.blueprint)
    app.register_blueprint(auth_routes.blueprint)


    ''' Rest-x INIT '''
    from project.apis import blueprint as api
    app.register_blueprint(api)


    return app