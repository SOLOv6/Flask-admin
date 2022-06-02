# Libraries
from project import db
from sqlalchemy import func


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id', ondelete='CASCADE'))
    path_original = db.Column(db.String(200), unique=True, nullable=False)
    created_on = db.Column(db.DateTime(), server_default=func.now())
    is_damaged_1 = db.Column(db.Boolean(), nullable=True)
    is_damaged_2 = db.Column(db.Boolean(), nullable=True)
    is_damaged_3 = db.Column(db.Boolean(), nullable=True)
    is_damaged_4 = db.Column(db.Boolean(), nullable=True)
    is_damaged_5 = db.Column(db.Boolean(), nullable=True)
    is_damaged_6 = db.Column(db.Boolean(), nullable=True)
    conf_score = db.Column(db.Float, nullable=True)
    
    # Set Backref
    user = db.relationship('User', backref=db.backref('user_set'))
    car = db.relationship('Car', backref=db.backref('car_set'))