from datetime import datetime
from sqlalchemy import func
from lib.db.models import User, Category, Transaction

def create_user(session, username, email):
    user = User(username=username, email=email)
    return user.create(session)

def delete_user(session, user_id):
    return User.delete(session, user_id)

def list_users(session):
    return User.get_all(session)

def find_user_by_username(session, username):
    return User.find_by_username(session, username)

def create_category(session, username, name):
    user = User.find_by_username(session, username)
    if not user:
        raise ValueError("User not found")
    category = Category(name=name, user_id=user.id)
    return category.create(session)

def create_transaction(session, username, amount, type, category_name, description, date):
    user = User.find_by_username(session, username)
    category = session.query(Category).filter_by(name=category_name, user_id=user.id).first()
    if not user or not category:
        raise ValueError("User or category not found")
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    transaction = Transaction(
        amount=amount, type=type, category_id=category.id,
        user_id=user.id, date=date_obj, description=description
    )
    return transaction.create(session)

def generate_expense_report(session, username):
    user = User.find_by_username(session, username)
    if not user:
        raise ValueError("User not found")
    result = session.query(Category.name, func.sum(Transaction.amount).label('total')).\
        join(Transaction).\
        filter(Transaction.user_id == user.id, Transaction.type == 'expense').\
        group_by(Category.name).all()
    return {name: total for name, total in result}
