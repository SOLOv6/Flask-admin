# Libraries
from flask import g
from flask_restx import Namespace, Resource, fields, reqparse

# DB Models
from project.models.car import Car as CarModel

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
post_parser.add_argument('car_name', required=True, help='car_name', location='form')

# Create Put Parser
put_parser = post_parser.copy()
put_parser.replace_argument('car_name', required=False, help='car_name', location='form')


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
        car_name = args['car_name']
        car = CarModel(car_name = car_name)
        g.db.add(car)
        g.db.commit()
        return car, 201


# /api/cars/{id}
@ns.route('/<int:id>')
@ns.param('id', 'car_id')
class Car(Resource):
    @ns.expect(put_parser)
    @ns.marshal_list_with(car, skip_none=True)
    def put(self, id):
        """Update Car"""
        args = put_parser.parse_args()
        car = CarModel.query.get_or_404(id)
        if args['car_name'] is not None:
            car.car_name = args['car_name']
        g.db.commit()
        return car, 200

    def delete(self, id):
        """Delete Car"""
        car = CarModel.query.get_or_404(id)
        g.db.delete(car)
        g.db.commit()
        return '', 204