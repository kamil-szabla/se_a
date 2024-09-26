# models.py
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')
    devices = db.relationship('Device', foreign_keys='Device.assignee_id', back_populates='assignee', lazy=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    prod_year = db.Column(db.Integer, nullable=False)
    dtid = db.Column(db.String(50), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=True)
    firmware_version = db.Column(db.String(50), nullable=True)
    os_version = db.Column(db.String(50), nullable=True)
    last_fw_update = db.Column(db.DateTime, nullable=True)
    known_issues = db.Column(db.Text, nullable=True)
    related_tickets = db.Column(db.Text, nullable=True)

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_device_assignee_id'), nullable=True)
    assignee = db.relationship('User', foreign_keys=[assignee_id], back_populates='devices')

    status = db.Column(db.String(50), nullable=False, default='active')
    other_details = db.Column(db.Text, nullable=True)

    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)