# Libraries
from project import db
from sqlalchemy import func


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), unique=True, nullable=False)

    # Inference
    is_inferenced = db.Column(db.Boolean(), default=True, nullable=False)
    inferenced_on = db.Column(db.DateTime(), server_default=func.now())
    path_inference_dent = db.Column(db.String(200),unique=True, nullable=False)
    path_inference_scratch = db.Column(db.String(200),unique=True, nullable=False)
    path_inference_spacing = db.Column(db.String(200),unique=True, nullable=False)

    # Inspect
    is_inspected = db.Column(db.Boolean(), default=False, nullable=False)
    inspected_on = db.Column(db.DateTime(), nullable=True)
    path_inspect_dent = db.Column(db.String(200),unique=True, nullable=True)
    path_inspect_scratch = db.Column(db.String(200),unique=True, nullable=True)
    path_inspect_spacing = db.Column(db.String(200),unique=True, nullable=True)
    inspector = db.Column(db.String(20), nullable=True)

    # Set Backref
    event = db.relationship('Event', backref=db.backref('event_set'))