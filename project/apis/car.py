from flask import g
from flask_restx import Namespace, Resource, fields, reqparse
from project.models.models import Car as CarModel

# Define Namespace
ns = Namespace(
    'cars',
    description='CAR API'
)

# Create Model to Namespace
car = ns.model('Car',{
    'id': fields.Integer(required=True, description='car_id'),
    'car_name': fields.String(required=True, description='car_name'),
    'registered_on': fields.DateTime(description='register_date'),
})

# Create Post Parser
post_parser = reqparse.RequestParser()
post_parser.add_argument('id', required=True, help='car_id')
post_parser.add_argument('car_name', required=True, help='car_name')

# /api/cars
@ns.route('')
class CarList(Resource):
    @ns.marshal_list_with(car, skip_none=True)
    def get(self):
        """Get All Cars"""
        data = CarModel.query.all()
        return data, 200

    @ns.expect(post_parser)
    @ns.marshal_list_with(car, skip_none=True)
    def post(self):
        """Create Car"""
        args = post_parser.parse_args()
        id = args['id']
        car_name = args['car_name']