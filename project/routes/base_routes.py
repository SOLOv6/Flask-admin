# Libraries
from flask import Blueprint, render_template

# DB
from project.models.car import Car as CarModel


blueprint = Blueprint(
    'base',
    __name__
)

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/cars')
def cars():
    car_list = CarModel.query.order_by(CarModel.registered_on.desc())
    return render_template('cars.html', car_list=car_list)