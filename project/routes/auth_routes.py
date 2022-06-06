# Libraries
from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from werkzeug import security

# DB Models
from project import db
from project.models.admin import Admin as AdminModel

# Flask Forms
from project.form.auth_form import LoginForm, RegisterForm


blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


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
        # TODO
        # 1) 유저 조회
        # 2) 유저가 이미 존재하는지 확인
        # 3) 없으면 유저 생성
        # 4) 로그인 유지(Session)
        admin_name = form.data.get('admin_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        admin = AdminModel.find_one_by_admin_name(admin_name)
        if admin:
            flash('Admin Name already exists.')
            return redirect(request.path)
        else:
            db.session.add(
                AdminModel(
                    admin_name=admin_name,
                    password=security.generate_password_hash(password)
                )
            )
            db.session.commit()
            session['admin_name'] = admin.admin_name
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