import click
from lib.db import Session
from lib.helpers import create_user, delete_user, list_users, find_user_by_username, create_category, create_transaction, generate_expense_report

@click.group()
def cli():
    """Personal Finance Manager CLI"""
    pass

@cli.command()
@click.option('--username', prompt='Username', help='Unique username')
@click.option('--email', prompt='Email', help='User email')
def register(username, email):
    """Register a new user"""
    with Session() as session:
        try:
            user = create_user(session, username, email)
            click.echo(f"User {user.username} created with ID {user.id}")
        except ValueError as e:
            click.echo(f"Error: {e}")

@cli.command(name='delete-user')
@click.option('--user-id', type=int, prompt='User ID', help='ID of user to delete')
def delete_user_cmd(user_id):
    """Delete a user by ID"""
    with Session() as session:
        user = delete_user(session, user_id)
        if user:
            click.echo(f"User {user.username} deleted successfully!")
        else:
            click.echo("User not found")

@cli.command(name='list-users')
def list_users_cmd():
    """List all users"""
    with Session() as session:
        users = list_users(session)
        for user in users:
            click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

@cli.command()
@click.option('--username', prompt='Username', help='Username to find')
def find_user(username):
    """Find a user by username"""
    with Session() as session:
        user = find_user_by_username(session, username)
        if user:
            click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
        else:
            click.echo("User not found")

@cli.command()
@click.option('--username', prompt='Username', help='Username of the user')
@click.option('--name', prompt='Category name', help='Name of the category')
def add_category(username, name):
    """Add a category for a user"""
    with Session() as session:
        try:
            category = create_category(session, username, name)
            click.echo(f"Category {category.name} created successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")

@cli.command()
@click.option('--username', prompt='Username', help='Username of the user')
@click.option('--amount', type=float, prompt='Amount', help='Transaction amount')
@click.option('--type', prompt='Type (income/expense)', help='Transaction type')
@click.option('--category', prompt='Category', help='Category name')
@click.option('--description', prompt='Description', help='Transaction description')
@click.option('--date', prompt='Date (YYYY-MM-DD)', help='Transaction date')
def add_transaction(username, amount, type, category, description, date):
    """Add a transaction for a user"""
    with Session() as session:
        try:
            transaction = create_transaction(session, username, amount, type, category, description, date)
            click.echo(f"Transaction added successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")

@cli.command()
@click.option('--username', prompt='Username', help='Username for the report')
def view_report(username):
    """View expense report by category for a user"""
    with Session() as session:
        try:
            report = generate_expense_report(session, username)
            if report:
                click.echo("Expense Report by Category:")
                for category, total in report.items():
                    click.echo(f"{category}: ${total:.2f}")
            else:
                click.echo("No expenses found")
        except ValueError as e:
            click.echo(f"Error: {e}")

if __name__ == '__main__':
    cli()