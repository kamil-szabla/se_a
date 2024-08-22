# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from mypackage.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ITAssetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
