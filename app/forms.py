# forms.py
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField, SelectField, DateTimeField, ValidationError
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User

def get_users():
    return User.query

def password_strength_check(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character.')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_strength_check])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DeviceForm(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    prod_year = IntegerField('Production Year', validators=[DataRequired()])
    dtid = StringField('Device Type ID', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional()])
    firmware_version = StringField('Firmware Version', validators=[Optional()])
    os_version = StringField('OS Version', validators=[Optional()])
    last_fw_update = DateField('Last Firmware Update', format='%Y-%m-%d', validators=[Optional()])
    known_issues = TextAreaField('Known Issues', validators=[Optional()])
    related_tickets = TextAreaField('Related Tickets', validators=[Optional()])
    assignee = QuerySelectField(
        'Assignee',
        query_factory=get_users,
        get_label='username',
        allow_blank=True,
        blank_text='Select a user',

    )
    status = SelectField('Status', choices=[('active', 'Active'), ('in repair', 'In Repair'), ('broken', 'Broken')], validators=[Optional()])
    other_details = TextAreaField('Other Details', validators=[Optional()])
    submit = SubmitField('Save Device')

    def __init__(self, *args, **kwargs):
        # Capture the update flag and the obj to identify the current device
        self.update = kwargs.pop('update', False)
        self.obj = kwargs.get('obj')  # Capture the object if passed for updates
        super(DeviceForm, self).__init__(*args, **kwargs)

        if self.update:
            # Set dtid field to read-only in the template
            self.dtid.render_kw = {'readonly': True}

    def validate_dtid(self, field):
        from app.models import Device
        if self.update and self.obj:
            # Skip uniqueness validation if updating and dtid matches the current device's dtid
            existing_device = Device.query.filter_by(dtid=field.data).first()
            if existing_device and existing_device.id != self.obj.id:
                raise ValidationError('Device Type ID must be unique. This ID is already in use.')
        else:
            # Regular uniqueness validation for new devices
            existing_device = Device.query.filter_by(dtid=field.data).first()
            if existing_device:
                raise ValidationError('Device Type ID must be unique. This ID is already in use.')


class DeviceFilterForm(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[Optional()])
    model = StringField('Model', validators=[Optional()])
    firmware_version = StringField('Firmware Version', validators=[Optional()])
    assignee = QuerySelectField(
        'Assignee',
        query_factory=get_users,
        get_label='username',
        allow_blank=True,
        blank_text='Any Assignee',
        validators=[Optional()]
    )
    location = StringField('Location', validators=[Optional()])
    submit = SubmitField('Filter')
