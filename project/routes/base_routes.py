# Libraries
from flask import Blueprint, render_template, request, g
from sqlalchemy import and_, func

# DB Models
from project.models.event import Event as EventModel
from project.models.entry import Entry as EntryModel

blueprint = Blueprint(
    'base',
    __name__
)

# Get Event List Route
@blueprint.route('/')
def index():
    input_from = request.args.get('input_from', default='')
    input_to = request.args.get('input_to', default='')
    page = request.args.get('page', type=int ,default=1)
    needle = request.args.get('needle', type=str, default='')
    event_list = EventModel.query.order_by(EventModel.created_on.desc())
    if needle:
        event_list = event_list.filter(
            EventModel.id.ilike(needle)
        )
    if input_from and input_to:
        event_list = event_list.filter(and_
            (func.date(EventModel.created_on) >= input_from),
            (func.date(EventModel.created_on) <= input_to)
        )
    event_list = event_list.paginate(page, per_page=10)
    return render_template('index.html', event_list=event_list, page=page)

# Get Event Detail Route
@blueprint.route('/detail/<int:id>')
def detail(id):
    entry = EntryModel.query.filter(EntryModel.event_id == id).first()
    return render_template('detail.html', entry=entry)