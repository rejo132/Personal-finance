import click
from lib.db import Session
from lib.db.models import User
from lib.helpers import (
    create_user, create_category, create_transaction,
    delete_user, list_users, find_user_by_username,
    generate_expense_report
)

@click.group()
def cli():
    pass

@click.command()
@click.option('--username', prompt='Username', help='Unique username')
@click.option('--email', prompt='Email', help='User email')
def register(username, email):
    with Session() as session:
        try:
            create_user(session, username, email)
            click.echo(f"User {username} created successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")

@click.command()
@click.option('--id', prompt='User ID', type=int, help='User ID to delete')
def delete_user(id):
    with Session() as session:
        try:
            user = delete_user(session, id)
            if user:
                click.echo(f"User {user.username} deleted successfully!")
            else:
                click.echo("User not found.")
        except ValueError as e:
                click.echo(f"Error: {e}")

@click.command()
def list_users():
    with Session():
        as session:
        users = list_users(session)
        click.echo("\nAll Users:")
        for user in users:
            click.echo(f"ID: {user.id}, Username: {user.id}, Email: {user.username}, Email:")
 {user.email}")

@click.command()
@click.option('--username', prompt='Username', help='Username to find')
def find_user(username):
    with Session() as session:
        user = find_user_by_username(session, username)
        if user:
            click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
        else:
            click.echo("User not found.")

@click.command()
@click.option('--username', prompt='Username', help='User to add category for')
@click.option('--name', prompt='Category Name', help='Category name')
def add_category(username, name):
    with Session() as session:
        try:
            create_category(session, username, name)
            click.echo(f"Category {name} created successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")

@click.command()
@click.option('--username', prompt='Username', help='User to add transaction for')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount')
@click.option('--type', prompt='Type', type=click.Choice(['income', 'expense']), help='Transaction type')
@click.option('--category', prompt='Category', help='Category name')
@click.option('--description', prompt='Description', help='Transaction description')
@click.option('--date', prompt='Date (YYYY-MM-DD)', help='Transaction date')
def add_transaction(username, amount, type, category, description, date):
    with Session() as session:
        try:
            create_transaction(session, username, amount, type, category, description, date)
            click.echo("Transaction added successfully!")
        except ValueError as e:
            click.echo(f"Error: {e}")

@click.command()
@click.option('--username', prompt='Username', help='User to view report for')
def view_report(username):
    with Session() as session:
        try:
            report = generate_expense_report(session, username)
            click.echo("\nExpense Report by Category:")
            for category, total in report.items():
                click.echo(f"{category}: ${total:.2f}")
        except ValueError as e:
            click.echo(f"Error: {e}")

@click.command()
def exit():
    click.echo("Goodbye!")
    import sys
    sys.exit()

cli.add_command(register)
cli.add_command(delete_user)
cli.add_command(list_users)
cli.add_command(find_user)
cli.add_command(add_category)
cli.add_command(add_transaction)
cli.add_command(view_report)
cli.add_command(exit)

if __name__ == '__main__':
    cli()
