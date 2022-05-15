# Libraries
from flask import Blueprint, render_template, request, g

# DB Models
from project.models.event import Event as EventModel

blueprint = Blueprint(
    'base',
    __name__
)

@blueprint.route('/')
def index():
    input_from = request.args.get('input_from', default=None)
    input_to = request.args.get('input_to', default=None)
    page = request.args.get('page',type=int ,default=1)
    event_list = EventModel.query.order_by(EventModel.created_on.desc())
    if input_from and input_to:
        pass
    event_list = event_list.paginate(page, per_page=10)
    return render_template('index.html', event_list=event_list, page=page)