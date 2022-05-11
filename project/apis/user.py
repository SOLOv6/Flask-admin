# Libraries
from flask import g
from flask_restx import Namespace, Resource, fields, reqparse

# DB Models
from project.models.user import User as UserModel

# Define Namespace
ns = Namespace(
    'users',
    description='User API'
)

# Create Model to Namespace
user = ns.model('User',{
    'id': fields.Integer(required=True, description='user_id'),
    'user_name': fields.String(required=True, description='user_name'),
    'registered_on': fields.DateTime(description='register_date'),
})

# Create Post Parser
post_parser = reqparse.RequestParser()
post_parser.add_argument('user_name', required=True, help='user_name', location='form')

# Create Put Parser
put_parser = post_parser.copy()
put_parser.replace_argument('user_name', required=False, help='user_name', location='form')


# /api/users
@ns.route('')
class UserList(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        """Get All Users"""
        data = UserModel.query.all()
        return data, 200

    @ns.expect(post_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        """Create User"""
        args = post_parser.parse_args()
        user_name = args['user_name']
        user = UserModel(user_name=user_name)
        g.db.add(user)
        g.db.commit()
        return user, 201

# /api/users/{id}
@ns.route('/<int:id>')
@ns.param('id', 'user_id')
class User(Resource):
    @ns.expect(put_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def put(self, id):
        """Update User"""
        args = put_parser.parse_args()
        user = UserModel.query.get_or_404(id)
        if args['user_name'] is not None:
            user.user_name = args['user_name']
        g.db.commit()
        return user, 200

    def delete(self, id):
        """Delete User"""
        user = UserModel.query.get_or_404(id)
        g.db.delete(user)
        g.db.commit()
        return '', 204