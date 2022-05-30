# Libraries
from project import db
from sqlalchemy import func


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(10), nullable=False)
    registered_on = db.Column(db.DateTime(), server_default=func.now())

    @classmethod
    def find_one_by_car_id(cls, car_id):
        return Car.query.filter_by(id=car_id).first()