# Libraries
from flask import Blueprint, render_template, request, g, url_for
from werkzeug.utils import redirect

# DB Models
from project.models.car import Car as CarModel


blueprint = Blueprint(
    'cars',
    __name__,
    url_prefix='/cars'
)

@blueprint.route('/')
def cars():
    car_list = CarModel.query.order_by(CarModel.registered_on)
    return render_template('cars.html', car_list=car_list)

@blueprint.route('/register', methods=['POST'])
def register():
    car_name = request.form['car_name']
    car = CarModel(car_name=car_name)
    g.db.add(car)
    g.db.commit()
    return redirect(url_for('cars.cars'))