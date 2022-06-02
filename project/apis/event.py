# Libraries
from flask import g
from flask_restx import Namespace, Resource, fields, reqparse, inputs

# DB Models
from project.models.event import Event as EventModel
from project.models.user import User as UserModel
from project.models.car import Car as CarModel

# Define Namespace
ns = Namespace(
    'events',
    description='Event API'
)

# Create Model to Namespace
event = ns.model('Event',{
    'id': fields.Integer(required=True, description='event_id'),
    'user_id': fields.Integer(required=True, description='user_id'),
    'car_id': fields.Integer(required=True, description='car_id'),
    'path_original': fields.String(required=True, description='path_original'),
    'created_on': fields.DateTime(description='created_on'),
    'is_damaged_1': fields.Boolean(description='is_damaged for first image'),
    'is_damaged_2': fields.Boolean(description='is_damaged for second image'),
    'is_damaged_3': fields.Boolean(description='is_damaged for third image'),
    'is_damaged_4': fields.Boolean(description='is_damaged for fourth image'),
    'is_damaged_5': fields.Boolean(description='is_damaged for fifth image'),
    'is_damaged_6': fields.Boolean(description='is_damaged for sixth image'),
    'conf_score': fields.Float(description='confidence_score'),
})

# Create Post Parser
post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', required=True, help='user_id', location='form')
post_parser.add_argument('car_id', required=True, help='car_id', location='form')
post_parser.add_argument('path_original', required=True, help='path_original', location='form')
post_parser.add_argument('is_damaged_1', required=False, type=inputs.boolean, help='is_damaged_1', location='form')
post_parser.add_argument('is_damaged_2', required=False, type=inputs.boolean, help='is_damaged_2', location='form')
post_parser.add_argument('is_damaged_3', required=False, type=inputs.boolean, help='is_damaged_3', location='form')
post_parser.add_argument('is_damaged_4', required=False, type=inputs.boolean, help='is_damaged_4', location='form')
post_parser.add_argument('is_damaged_5', required=False, type=inputs.boolean, help='is_damaged_5', location='form')
post_parser.add_argument('is_damaged_6', required=False, type=inputs.boolean, help='is_damaged_6', location='form')
post_parser.add_argument('conf_score', required=False, help='confidence_score', location='form')


# /api/events
@ns.route('')
class EventList(Resource):
    @ns.marshal_list_with(event, skip_none=True)
    def get(self):
        """Get All Events"""
        data = EventModel.query.all()
        return data, 200

    @ns.expect(post_parser)
    @ns.marshal_list_with(event, skip_none=True)
    def post(self):
        """Create Event"""
        args = post_parser.parse_args()
        user_id = args['user_id']
        car_id = args['car_id']
        path_original = args['path_original']
        is_damaged_1 = args['is_damaged_1']
        is_damaged_2 = args['is_damaged_2']
        is_damaged_3 = args['is_damaged_3']
        is_damaged_4 = args['is_damaged_4']
        is_damaged_5 = args['is_damaged_5']
        is_damaged_6 = args['is_damaged_6']
        conf_score = args['conf_score']
        
        # Validation
        user = UserModel.query.get(user_id)
        car = CarModel.query.get(car_id)
        if user is None:
            ns.abort(403, 'User does not exist.')
        if car is None:
            ns.abort(403, 'Car does not exist.')

        event = EventModel(
            user_id=user_id,
            car_id=car_id,
            path_original=path_original,
            is_damaged_1=is_damaged_1,
            is_damaged_2=is_damaged_2,
            is_damaged_3=is_damaged_3,
            is_damaged_4=is_damaged_4,
            is_damaged_5=is_damaged_5,
            is_damaged_6=is_damaged_6,
            conf_score=conf_score
        )
        g.db.add(event)
        g.db.commit()
        return event, 201

# api/events/{id}
@ns.route('/<int:id>')
@ns.param('id', 'event_id')
class Event(Resource):
    def delete(self, id):
        """Delete Event"""
        event = EventModel.query.get_or_404(id)
        g.db.delete(event)
        g.db.commit()
        return '', 204