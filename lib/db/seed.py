from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, User, Category, Transaction
from datetime import date

engine = create_engine('sqlite:///finance.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()

session.query(Transaction).delete()
session.query(Category).delete()
session.query(User).delete()

for _ in range(3):
    user = User(username=fake.user_name(), email=fake.email())
    user.create(session)

for user in User.get_all(session):
    for _ in range(2):
        category = Category(name=fake.word().capitalize(), user_id=user.id)
        category.create(session)
        for _ in range(3):
            transaction = Transaction(
                amount=fake.random_int(10, 200),
                type=fake.random_element(['income', 'expense']),
                category_id=category.id,
                user_id=user.id,
                date=fake.date_this_year(),
                description=fake.sentence()
            )
            transaction.create(session)

session.commit()
print("Database seeded successfully!")
