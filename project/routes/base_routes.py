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
    input_from = request.args.get('input_from')
    input_to = request.args.get('input_to')
    event_list = EventModel.query.order_by(EventModel.created_on.desc())
    if input_from and input_to:
        return render_template('index.html', event_list=event_list, input_from=input_from, input_to=input_to)
    return render_template('index.html', event_list=event_list)