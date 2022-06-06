# Libraries
from project import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)