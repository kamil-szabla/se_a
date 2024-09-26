import click
from flask.cli import with_appcontext
from app.models import User
from app import db

@click.command('create-admin')
@with_appcontext
def create_admin():
    """Create an admin user."""
    username = click.prompt("Enter admin username")
    email = click.prompt("Enter admin email")
    password = click.prompt("Enter admin password", hide_input=True, confirmation_prompt=True)

    if User.query.filter_by(username=username).first():
        click.echo(f"Error: Username '{username}' is already taken.")
        return

    if User.query.filter_by(email=email).first():
        click.echo(f"Error: Email '{email}' is already registered.")
        return

    admin_user = User(
        username=username,
        email=email,
        role='admin'
    )
    admin_user.password = password  # This will automatically hash the password

    db.session.add(admin_user)
    db.session.commit()
    click.echo(f"Admin user '{username}' created successfully.")

