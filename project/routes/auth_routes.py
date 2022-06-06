# Libraries
from flask import Blueprint, render_template

# DB Models
from project.models.admin import Admin as AdminModel

# Flask Forms
from project.form.auth_form import LoginForm, RegisterForm


blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

@blueprint.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@blueprint.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@blueprint.route('/logout')
def logout():
    return 'logout'