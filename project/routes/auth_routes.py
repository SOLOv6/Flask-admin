# Libraries
from flask import Blueprint

# DB Models
from project.models.admin import Admin as AdminModel

blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

@blueprint.route('/login')
def index():
    return "Hello, This is Admin Login Page!"