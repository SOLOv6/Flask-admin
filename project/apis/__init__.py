# Libraries
from flask import Blueprint, g, abort
from flask_restx import Api
from functools import wraps

# Namespaces
from .car import ns as CarNamespace
from .user import ns as UserNamespace
from .event import ns as EventNamespace
from .entry import ns as EntryNamespace


def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.admin:
            abort(401)
        return func(*args, **kwargs)
    return __wrapper

# Create '/api' Blueprint
blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)

# Add API on Blueprint
api = Api(
    blueprint,
    title='SOLOv6 API',
    version='1.0',
    doc='/docs',
    decorators=[check_session],
    description='Welcome to API docs!'
)

# Add Namespaces
api.add_namespace(CarNamespace, '/cars')
api.add_namespace(UserNamespace, '/users')
api.add_namespace(EventNamespace, '/events')
api.add_namespace(EntryNamespace, '/entries')