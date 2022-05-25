# Libraries
from flask import Blueprint, redirect, render_template, request, g, url_for
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
    event_list = EventModel.query.filter(
        EventModel.is_damaged != None
    ).order_by(
        EventModel.created_on.desc()
    )

    if needle:
        event_list = event_list.filter(
            EventModel.car_id == needle
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
    if entry is None:
        return render_template('detail.html', entry=entry)
    path_inference_list = entry.path_inference_dent.split('_')[:-1]
    return render_template('detail.html', entry=entry, path_inference_list=path_inference_list)

# Get Event Inspect Route
@blueprint.route('/detail/inspect')
def inspect():
    path_original = request.args['path_original']
    return render_template('via.html')

# Confirm Inspection
@blueprint.route('/detail/<int:id>/confirm', methods=['POST'])
def confirm(id):
    if request.method == 'POST':
        inspector = request.form['inspector']
        inspected_on = func.now()
        is_inspected = True
        entry = EntryModel.query.filter(EntryModel.event_id == id).first()
        entry.inspector = inspector
        entry.inspected_on = inspected_on
        entry.is_inspected = is_inspected
        g.db.commit()
        return redirect(url_for('base.detail', id=id))