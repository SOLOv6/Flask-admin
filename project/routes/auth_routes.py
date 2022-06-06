# Libraries
from flask import Blueprint, redirect, render_template, url_for, flash, session, request, g
from werkzeug import security

# DB Models
from project.models.admin import Admin as AdminModel

# Flask Forms
from project.form.auth_form import LoginForm, RegisterForm


blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

# Request Hook for entire app
@blueprint.before_app_request
def before_app_request():
    g.admin = None
    admin_name = session.get('admin_name')
    if admin_name:
        admin = AdminModel.find_one_by_admin_name(admin_name)
        if admin:
            g.admin = admin
        else:
            session.pop('admin_name', None)

# Get Login Route (Redirect)
@blueprint.route('/')
def index():
    return redirect(url_for('auth.login'))

# Get Login Route
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # check method 'POST' and validate is OK
    if form.validate_on_submit():
        admin_name = form.data.get('admin_name')
        password = form.data.get('password')
        admin = AdminModel.find_one_by_admin_name(admin_name)
        if admin:
            if not security.check_password_hash(admin.password, password):
                flash('Password is not valid.')
            else:
                session['admin_name'] = admin.admin_name
                return redirect(url_for('base.index'))

        else:
            flash('Admin Name does not exists.')
    else:
        flash_form_errors(form)

    return render_template('login.html', form=form)

# Get Register Route
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # check method 'POST' and validate is OK
    if form.validate_on_submit():
        admin_name = form.data.get('admin_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        admin = AdminModel.find_one_by_admin_name(admin_name)
        if admin:
            flash('Admin Name already exists.')
            return redirect(request.path)
        else:
            g.db.add(
                AdminModel(
                    admin_name=admin_name,
                    password=security.generate_password_hash(password)
                )
            )
            g.db.commit()
            session['admin_name'] = admin_name
            return redirect(url_for('base.index'))
    else:
        flash_form_errors(form)

    return render_template('register.html', form=form)

# Get Logout Route
@blueprint.route('/logout')
def logout():
    session.pop('admin_name', None)
    return redirect(url_for('auth.login'))


def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)