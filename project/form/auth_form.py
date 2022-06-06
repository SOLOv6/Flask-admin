# Libraries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    admin_name = StringField('Admin Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(LoginForm):
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), EqualTo(
            'repassword',
            message='Password must match.'
        )]
    )
    repassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )