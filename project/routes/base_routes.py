from flask import Blueprint

blueprint = Blueprint(
    'base',
    __name__
)

@blueprint.route('/')
def index():
    return "Hello, This is Admin Main Page!"