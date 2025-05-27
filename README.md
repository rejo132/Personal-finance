Personal Finance Manager CLI
A command-line application to manage personal finances by tracking income, expenses, and budget categories.
Setup

Clone the repository: git clone https://github.com/rejo132/personal_finance
Install dependencies: pipenv install
Enter virtual environment: pipenv shell
Initialize database: alembic revision --autogenerate -m "initial" && alembic upgrade head
(Optional) Seed data: python lib/db/seed.py
Run CLI: python -m lib.cli
Run tests: pipenv run pytest -v tests/test_helpers.py

Files

lib/cli.py: CLI using Click for user, category, and transaction management.
lib/db/models.py: SQLAlchemy models (User, Category, Transaction).
lib/db/seed.py: Seeds database with test data.
lib/helpers.py: Business logic for CRUD and reports.
lib/db/init.py: SQLAlchemy engine and session setup.
lib/debug.py: Debugging utilities.
tests/test_helpers.py: Unit tests for helper functions.

CLI Commands

register --username <name> --email <email>
delete-user --user-id <id>
list-users
find-user --username <name>
add-category --username <name> --name <category>
add-transaction --username <name> --amount <float> --type <income/expense> --category <name> --description <text> --date <YYYY-MM-DD>
view-report --username <name>
exit

Data Model

User: id, username (unique), email. One-to-many with Categories, Transactions.
Category: id, name, user_id. One-to-many with Transactions.
Transaction: id, amount, type, category_id, user_id, date, description.

Design Decisions

Click: Chosen for simplicity and robust option parsing.
SQLAlchemy ORM: Used for type safety and relationships, with cascade deletes.
SQLite: Lightweight database for CLI.
Modular Structure: Separates concerns for maintainability.
Unit Tests: Ensure helper function reliability.

Learning Goals

CLI: Interactive interface with Click.
SQLAlchemy ORM: Three related tables with relationships.
Pipenv: Dependency management.
Package Structure: Modular design.
Data Structures: Lists, dictionaries, tuples.

