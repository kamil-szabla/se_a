from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/')
@main_bp.route('/home')
@login_required
def home():
    return redirect(url_for('devices.dashboard'))
