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

# Cars Main
@blueprint.route('/')
def cars():
    car_list = CarModel.query.order_by(CarModel.registered_on)
    return render_template('cars.html', car_list=car_list)

# Register Car API
@blueprint.route('/register', methods=['POST'])
def register():
    car_name = request.form['car_name']
    car = CarModel(car_name=car_name)
    g.db.add(car)
    g.db.commit()
    return redirect(url_for('cars.cars'))

# Delete Car API
@blueprint.route('/delete', methods=['POST'])
def delete():
    car_id = request.form['car_id']
    car = CarModel.query.get_or_404(car_id)
    g.db.delete(car)
    g.db.commit()
    return redirect(url_for('cars.cars'))