import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import db, create_app
from app.models import User, Device

app = create_app()
with app.app_context():
    # Initialize the database
    db.create_all()

    # Optional: Add initial data
    # hashed_password = generate_password_hash('adminpassword').decode('utf-8')
    # admin_user = User(username='admin', email='admin@example.com', password=hashed_password, is_admin=True)
    # db.session.add(admin_user)
    # db.session.commit()
