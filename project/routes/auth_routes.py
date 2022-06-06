# Libraries
from flask import Blueprint, redirect, render_template, url_for

# DB Models
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
        # TODO
        # 1) 유저 조회
        # 2) 존재하는 유저인지 확인
        # 3) 패스워드 정합성 확인
        # 4) 로그인 유지(Session)
        admin_name = form.data.get('admin_name')
        password = form.data.get('password')
        return f'{admin_name}, {password}'
    else:
        # TODO: Error
        pass

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
        return f'{admin_name}, {password}, {repassword}'
    else:
        # TODO: Error
        pass

    return render_template('register.html', form=form)

# Get Logout Route
@blueprint.route('/logout')
def logout():
    return 'logout'