# Libraries
from flask import Blueprint, render_template, request, g, url_for
from werkzeug.utils import redirect

# DB Models
from project.models.user import User as UserModel


blueprint = Blueprint(
    'users',
    __name__,
    url_prefix='/users'
)

# Get User List Route
@blueprint.route('/')
def users():
    if not g.admin:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', type=int, default=1)
    needle = request.args.get('needle', type=str, default='')
    user_list = UserModel.query.order_by(UserModel.registered_on.desc())
    if needle:
        user_list = user_list.filter(
            UserModel.id.ilike(needle)
        )
    user_list = user_list.paginate(page, per_page=10)
    return render_template('users.html', user_list=user_list, page=page, needle=needle)

# Register User Route
@blueprint.route('/register', methods=['POST'])
def register():
    if not g.admin:
        return redirect(url_for('auth.login'))
    user_name = request.form['user_name']
    user = UserModel(user_name=user_name)
    g.db.add(user)
    g.db.commit()
    return redirect(url_for('users.users'))

# Delete User Route
@blueprint.route('/delete', methods=['POST'])
def delete():
    if not g.admin:
        return redirect(url_for('auth.login'))
    user_id = request.form['user_id']
    user = UserModel.query.get_or_404(user_id)
    g.db.delete(user)
    g.db.commit()
    return redirect(url_for('users.users'))