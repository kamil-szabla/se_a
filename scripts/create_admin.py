# scripts/create_admin.py
from mypackage import db, app
from mypackage.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        db.session.delete(admin_user)
        db.session.commit()

    hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
    admin_user = User(username='admin', email='admin@example.com',
                      password=hashed_password, role='admin')
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully!")
