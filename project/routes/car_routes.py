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

# Get Car List Route
@blueprint.route('/')
def cars():
    if not g.admin:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', type=int, default=1)
    needle = request.args.get('needle', type=str, default='')
    car_list = CarModel.query.order_by(CarModel.registered_on.desc())
    if needle:
        car_list = car_list.filter(
            CarModel.id.ilike(needle)
        )
    car_list = car_list.paginate(page, per_page=10)
    return render_template('cars.html', car_list=car_list, page=page, needle=needle)

# Register Car Route
@blueprint.route('/register', methods=['POST'])
def register():
    if not g.admin:
        return redirect(url_for('auth.login'))
    car_name = request.form['car_name']
    car = CarModel(car_name=car_name)
    g.db.add(car)
    g.db.commit()
    return redirect(url_for('cars.cars'))

# Delete Car Route
@blueprint.route('/delete', methods=['POST'])
def delete():
    if not g.admin:
        return redirect(url_for('auth.login'))
    car_id = request.form['car_id']
    car = CarModel.query.get_or_404(car_id)
    g.db.delete(car)
    g.db.commit()
    return redirect(url_for('cars.cars'))