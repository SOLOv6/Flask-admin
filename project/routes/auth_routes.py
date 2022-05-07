from flask import Blueprint

blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

@blueprint.route('/login')
def index():
    return "Hello, This is Admin Login Page!"