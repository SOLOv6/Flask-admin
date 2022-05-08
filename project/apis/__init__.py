from flask import Blueprint
from flask_restx import Api
from .car import ns as CarNamespace

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
    description='Welcome to API docs!'
)

# Add Namespaces
api.add_namespace(CarNamespace)