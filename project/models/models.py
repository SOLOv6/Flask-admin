from email.policy import default
from project import db
from sqlalchemy import func

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(10), nullable=False)
    registered_on = db.Column(db.DateTime(), default=func.now())