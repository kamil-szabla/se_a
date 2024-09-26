from os import abort
from functools import wraps
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.forms import DeviceForm, DeviceFilterForm
from app.models import Device, User
from datetime import datetime

devices_bp = Blueprint('devices', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Dashboard (list all devices)
@devices_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DeviceFilterForm(request.args)
    query = Device.query

    if form.validate():
        if form.manufacturer.data:
            query = query.filter(Device.manufacturer.ilike(f'%{form.manufacturer.data}%'))
        if form.model.data:
            query = query.filter(Device.model.ilike(f'%{form.model.data}%'))
        if form.assignee.data:
            query = query.filter(Device.assignee_id == form.assignee.data.id)
        if form.firmware_version.data:
            query = query.filter(Device.firmware_version.ilike(f'%{form.firmware_version.data}%'))
        if form.location.data:
            query = query.filter(Device.location.ilike(f'%{form.location.data}%'))
    devices = query.all()
    return render_template('devices.html', devices=devices, form=form)

# Route to display devices assigned to the current user
@devices_bp.route('/my-devices')
@login_required
def my_devices():
    devices = Device.query.filter_by(assignee=current_user).all()
    return render_template('my_devices.html', devices=devices)

# Add a new device
@devices_bp.route('/devices/new', methods=['GET', 'POST'])
@login_required
def new_device():
    device_form = DeviceForm()
    if device_form.validate_on_submit():
        device = Device(
            manufacturer=device_form.manufacturer.data,
            model=device_form.model.data,
            prod_year=device_form.prod_year.data,
            dtid=device_form.dtid.data,
            location=device_form.location.data,
            firmware_version=device_form.firmware_version.data,
            os_version=device_form.os_version.data,
            last_fw_update=device_form.last_fw_update.data,
            known_issues=device_form.known_issues.data,
            related_tickets=device_form.related_tickets.data,
            assignee=device_form.assignee.data if device_form.assignee.data else None,
            status=device_form.status.data,
            other_details=device_form.other_details.data
        )
        db.session.add(device)
        db.session.commit()
        flash('Device added successfully!', 'success')
        return redirect(url_for('devices.dashboard'))
    else:
        print(device_form.errors)
    return render_template('create_device.html', title='Add Device', device_form=device_form)


# Device details page
@devices_bp.route('/devices/<int:device_id>', methods=['GET'])
@login_required
def device_details(device_id):
    device = Device.query.get_or_404(device_id)

    device_form = DeviceForm()

    return render_template('device_details.html', device=device,
                            device_form=device_form)

# Update existing device details
@devices_bp.route('/devices/<int:device_id>/update', methods=['GET', 'POST'])
@login_required
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    device_form = DeviceForm(obj=device, update=True)

    if device_form.validate_on_submit():

        # if device_form.dtid.data != device.dtid:
        #     flash("You cannot modify the Device Type ID.", "danger")
        #     return redirect(url_for('devices.update_device', device_id=device.id))

        device.manufacturer = device_form.manufacturer.data
        device.model = device_form.model.data
        device.prod_year = device_form.prod_year.data
        device.location = device_form.location.data
        device.firmware_version = device_form.firmware_version.data
        device.os_version = device_form.os_version.data
        device.known_issues = device_form.known_issues.data
        device.related_tickets = device_form.related_tickets.data
        device.assignee = device_form.assignee.data if device_form.assignee.data else None
        device.status = device_form.status.data

        # Commit all changes to the database
        try:
            db.session.commit()
            flash('Device updated successfully!', 'success')
            return redirect(url_for('devices.dashboard', device_id=device.id))
        except Exception as e:
            print(f"Error while committing: {e}")
            db.session.rollback()
            flash('An error occurred while updating the device.', 'danger')
    else:
        print(device_form.errors)
    return render_template('update_device.html', title='Update Device', device_form=device_form)

# Delete a device
@devices_bp.route('/devices/<int:device_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_device(device_id):
    if not current_user.is_admin:
        abort(403)

    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    flash('Device deleted successfully!', 'success')
    return redirect(url_for('devices.dashboard'))

