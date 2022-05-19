# Libraries
from flask import g
from flask_restx import Namespace, Resource, fields, reqparse, inputs
from sqlalchemy import func

# DB Models
from project.models.event import Event as EventModel
from project.models.entry import Entry as EntryModel

# Define Namespace
ns = Namespace(
    'entries',
    description='Entry API'
)

# Create Model to Namespace
entry = ns.model('Entry',{
    'id': fields.Integer(required=True, description='entry_id'),
    'event_id': fields.Integer(required=True, description='event_id'),
    'is_inferenced': fields.Boolean(required=True, description='is_inferenced'),
    'inferenced_on': fields.DateTime(required=True, description='inferenced_on'),
    'path_inference_dent': fields.String(required=True, description='path_inference_dent'),
    'path_inference_scratch': fields.String(required=True, description='path_inference_scratch'),
    'path_inference_spacing': fields.String(required=True, description='path_inference_spacing'),
    'is_inspected': fields.Boolean(required=False, description='is_inspected'),
    'inspected_on': fields.String(required=False, description='inspected_on'),
    'path_inspect_dent': fields.String(required=False, description='path_inspect_dent'),
    'path_inspect_scratch': fields.String(required=False, description='path_inspect_scratch'),
    'path_inspect_spacing': fields.String(required=False, description='path_inspect_spacing'),
    'inspector': fields.String(required=False, description='inspector'),
})

# Create Post Parser
post_parser = reqparse.RequestParser()
post_parser.add_argument('event_id', required=True, help='event_id', location='form')
post_parser.add_argument('path_inference_dent', required=True, help='path_inference_dent', location='form')
post_parser.add_argument('path_inference_scratch', required=True, help='path_inference_scratch', location='form')
post_parser.add_argument('path_inference_spacing', required=True, help='path_inference_spacing', location='form')

# Create Put Parser for Confirm
put_parser = post_parser.copy()
put_parser.remove_argument('event_id')
put_parser.remove_argument('path_inference_dent')
put_parser.remove_argument('path_inference_scratch')
put_parser.remove_argument('path_inference_spacing')
put_parser.add_argument('is_inspected', required=True, type=inputs.boolean , help='is_inspected', location='form')
put_parser.add_argument('inspector', required=True, help='inspector', location='form')


# /api/entries
@ns.route('')
class EntryList(Resource):
    @ns.marshal_list_with(entry, skip_none=True)
    def get(self):
        """Get All Entries"""
        data = EntryModel.query.all()
        return data, 200

    @ns.expect(post_parser)
    @ns.marshal_list_with(entry, skip_none=True)
    def post(self):
        """Create Entry"""
        args = post_parser.parse_args()
        event_id = args['event_id']
        path_inference_dent = args['path_inference_dent']
        path_inference_scratch = args['path_inference_scratch']
        path_inference_spacing = args['path_inference_spacing']

        # Validation
        event = EventModel.query.get(event_id)
        if event is None:
            ns.abort(400, 'Event does not exist.')

        entry = EntryModel(
            event_id=event_id,
            path_inference_dent=path_inference_dent,
            path_inference_scratch=path_inference_scratch,
            path_inference_spacing=path_inference_spacing
        )
        g.db.add(entry)
        g.db.commit()
        return entry, 201

# /api/entries/{id}
@ns.route('/<int:id>')
@ns.param('id', 'entry_id')
class Entry(Resource):
    def delete(self, id):
        """Delete Entry"""
        entry = EntryModel.query.get_or_404(id)
        g.db.delete(entry)
        g.db.commit()
        return '', 204

    @ns.expect(put_parser)
    @ns.marshal_list_with(entry, skip_none=True)
    def put(self, id):
        """Inspect Confirm"""
        args = put_parser.parse_args()
        entry = EntryModel.query.get_or_404(id)
        entry.is_inspected = args['is_inspected']
        entry.inspector = args['inspector']
        entry.inspected_on = func.now()
        g.db.commit()
        return entry, 200