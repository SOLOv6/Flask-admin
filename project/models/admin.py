# Libraries
from project import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    @classmethod
    def find_one_by_admin_name(cls, admin_name):
        return Admin.query.filter_by(admin_name=admin_name).first()