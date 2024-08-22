from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from mypackage import app, db, bcrypt
from mypackage.forms import RegistrationForm, LoginForm, ITAssetForm
from mypackage.models import User, ITAsset

@app.route("/")
@app.route("/home")
@login_required
def home():
    itassets = ITAsset.query.all()
    return render_template('home.html', itassets=itassets)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/itassets/new", methods=['GET', 'POST'])
@login_required
def create_itasset():
    form = ITAssetForm()
    if form.validate_on_submit():
        itasset = ITAsset(name=form.name.data, description=form.description.data, purchase_date=form.purchase_date.data, user_id=current_user.id)
        db.session.add(itasset)
        db.session.commit()
        flash('Your asset has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_itasset.html', title='New IT Asset', form=form)

@app.route("/itassets/<int:itasset_id>/update", methods=['GET', 'POST'])
@login_required
def update_itasset(itasset_id):
    itasset = ITAsset.query.get_or_404(itasset_id)
    if itasset.user != current_user and current_user.role != 'admin':
        abort(403)
    form = ITAssetForm()
    if form.validate_on_submit():
        itasset.name = form.name.data
        itasset.description = form.description.data
        itasset.purchase_date = form.purchase_date.data
        db.session.commit()
        flash('Your asset has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = itasset.name
        form.description.data = itasset.description
        form.purchase_date.data = itasset.purchase_date
    return render_template('create_itasset.html', title='Update IT Asset', form=form)

@app.route("/itassets/<int:itasset_id>/delete", methods=['POST'])
@login_required
def delete_itasset(itasset_id):
    itasset = ITAsset.query.get_or_404(itasset_id)
    if itasset.user != current_user and current_user.role != 'admin':
        abort(403)
    db.session.delete(itasset)
    db.session.commit()
    flash('Your asset has been deleted!', 'success')
    return redirect(url_for('home'))
