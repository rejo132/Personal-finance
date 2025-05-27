from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from lib.db.models import User, Category, Transaction

# Create a new user with unique username and email
def create_user(session, username, email):
    user = User(username=username, email=email)
    try:
        return user.create(session)
    except IntegrityError:
        session.rollback()
        raise ValueError("Username already exists")

# Delete a user by ID, return user or None
def delete_user(session, user_id):
    return User.delete(session, user_id)

# List all users in the database
def list_users(session):
    return User.get_all(session)

# Find a user by username, return user or None
def find_user_by_username(session, username):
    return User.find_by_username(session, username)

# Create a category for a user
def create_category(session, username, name):
    user = User.find_by_username(session, username)
    if not user:
        raise ValueError("User not found")
    category = Category(name=name, user_id=user.id)
    try:
        return category.create(session)
    except IntegrityError:
        session.rollback()
        raise ValueError("Category already exists for this user")

# Create a transaction with validation
def create_transaction(session, username, amount, type, category_name, description, date):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if type not in ['income', 'expense']:
        raise ValueError("Type must be 'income' or 'expense'")
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    user = User.find_by_username(session, username)
    if not user:
        raise ValueError("User not found")
    category = session.query(Category).filter_by(name=category_name, user_id=user.id).first()
    if not category:
        raise ValueError("Category not found")
    transaction = Transaction(
        amount=amount,
        type=type,  # Use string directly
        category_id=category.id,
        user_id=user.id,
        date=date_obj,
        description=description
    )
    return transaction.create(session)

# Generate expense report by category for a user
def generate_expense_report(session, username):
    user = User.find_by_username(session, username)
    if not user:
        raise ValueError("User not found")
    result = session.query(Category.name, func.sum(Transaction.amount).label('total')).\
        join(Transaction).\
        filter(Transaction.user_id == user.id, Transaction.type == 'expense').\
        group_by(Category.name).\
        having(func.sum(Transaction.amount) > 0).all()
    return {name: total for name, total in result}