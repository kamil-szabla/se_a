# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__, template_folder='../templates')

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initlize Flask-login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import routes
